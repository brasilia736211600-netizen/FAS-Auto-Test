"""Minimal portable command-line entry point for FAS."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

from fas_fallback import candidate_models, run_with_fallback
from fas_github import dispatch_workflow
from fas_git import (
    PUSH_FAILED_CODE,
    SCOPE_VIOLATION_CODE,
    PushFailedError,
    ScopeViolationError,
    changed_after,
    commit_if_changed,
    safe_push,
    status_porcelain,
)
from fas_recovery import build_scope_diagnosis_task
from fas_runtime import init_repository, read_state, record_test, select_route, write_state
from fas_watch import watch_and_recover
from model_router import TaskSignals, available_models


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fas")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="initialize durable FAS state")
    init.add_argument("repo", nargs="?", default=".")
    run = sub.add_parser("run", help="run one task through OpenCode")
    run.add_argument("task")
    run.add_argument("--repo", default=".")
    run.add_argument("--files-changed", type=int, default=1)
    run.add_argument("--ambiguity", type=int, default=0)
    run.add_argument("--architecture-impact", action="store_true")
    run.add_argument("--recovery", action="store_true")
    run.add_argument("--exploration", action="store_true")
    run.add_argument("--critical-review", action="store_true")
    run.add_argument("--latency-sensitive", action="store_true")
    run.add_argument("--test-cmd")
    watch = sub.add_parser("watch", help="watch CI for HEAD and perform bounded recovery")
    watch.add_argument("--repo", default=".")
    watch.add_argument("--max-attempts", type=int, default=3)
    watch.add_argument("--poll-limit", type=int, default=60)
    watch.add_argument("--poll-seconds", type=float, default=5.0)
    watch.add_argument("--workflow", help="optional workflow to dispatch when no CI run exists for HEAD")
    watch.add_argument("--test-cmd")
    return parser


def _run_task(args: argparse.Namespace) -> int:
    repo = Path(args.repo).expanduser().resolve()
    state_file = repo / ".fas" / "state.json"
    if not state_file.exists():
        init_repository(repo)
    state = read_state(repo)

    signals = TaskSignals(
        files_changed=args.files_changed,
        ambiguity=args.ambiguity,
        architecture_impact=args.architecture_impact,
        recovery=args.recovery,
        exploration=args.exploration,
        critical_review=args.critical_review,
        latency_sensitive=args.latency_sensitive,
    )
    planned_route = select_route(repo, signals)
    configured = available_models()[planned_route["capability"]]
    override = os.environ.get("FAS_MODEL")
    candidates = tuple(
        dict.fromkeys(
            ((override,) if override else ())
            + candidate_models(_route_decision(planned_route), configured)
        )
    )
    baseline = status_porcelain(str(repo))

    def retry_only_if_repository_unchanged(_attempt: object) -> bool:
        return not changed_after(str(repo), baseline)

    result = run_with_fallback(
        lambda model: ["opencode", "run", "--auto", "--model", model, "--agent", "build", args.task],
        candidates,
        cwd=str(repo),
        max_attempts=state.get("max_attempts", 3),
        should_retry=retry_only_if_repository_unchanged,
    )

    state = read_state(repo)
    state["phase"] = "EXECUTE"
    state["attempt"] = len(result.attempts)
    state["route"] = dict(planned_route)
    state["route"]["effective_model"] = result.selected_model
    state["route"]["attempts"] = [
        {
            "model": attempt.model,
            "returncode": attempt.returncode,
            "duration_seconds": round(attempt.duration_seconds, 3),
        }
        for attempt in result.attempts
    ]
    write_state(repo, state)

    if not result.success:
        return result.attempts[-1].returncode if result.attempts else 1

    test_cmd = args.test_cmd or os.environ.get("FAS_TEST_CMD")
    if test_cmd:
        test_start = time.monotonic()
        test = subprocess.run(test_cmd, cwd=repo, shell=True, check=False)
        record_test(
            repo,
            test_cmd,
            "PASS" if test.returncode == 0 else f"FAIL:{test.returncode}",
            time.monotonic() - test_start,
        )
        if test.returncode != 0:
            return test.returncode

    if os.environ.get("FAS_COMMIT") == "1":
        allowed_paths = None
        if args.recovery:
            allowed_paths = tuple(
                path.strip()
                for path in os.environ.get("FAS_ALLOWED_PATHS", "").splitlines()
                if path.strip()
            )
            if not allowed_paths:
                state = read_state(repo)
                state.setdefault("failure", {})["class"] = "scope_unknown"
                write_state(repo, state)
                return SCOPE_VIOLATION_CODE
        try:
            commit_sha = commit_if_changed(
                str(repo),
                os.environ.get("FAS_COMMIT_MESSAGE", "chore: FAS autonomous change"),
                allowed_paths=allowed_paths,
            )
        except ScopeViolationError:
            state = read_state(repo)
            state.setdefault("failure", {})["class"] = "scope_violation"
            write_state(repo, state)
            return SCOPE_VIOLATION_CODE
        state = read_state(repo)
        state["git"]["commit_sha"] = commit_sha
        write_state(repo, state)

    if os.environ.get("FAS_PUSH") == "1":
        try:
            safe_push(str(repo))
        except PushFailedError:
            state = read_state(repo)
            state.setdefault("failure", {})["class"] = "push_failed"
            write_state(repo, state)
            return PUSH_FAILED_CODE

    return 0


def _diagnose_scope(repo: str, task: str) -> str:
    """Run a read-only recovery diagnosis with bounded model fallback."""
    signals = TaskSignals(recovery=True, exploration=True)
    decision = _route_decision(select_route(Path(repo), signals))
    candidates = candidate_models(decision, available_models()[decision.capability.value])
    baseline = status_porcelain(repo)
    max_attempts = read_state(repo).get("max_attempts", 3)
    for model in candidates[:max_attempts]:
        result = subprocess.run(
            ["opencode", "run", "--auto", "--model", model, "--agent", "explore", task],
            cwd=repo,
            capture_output=True,
            text=True,
            check=False,
        )
        if status_porcelain(repo) != baseline:
            return ""
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
    return ""


def _watch(args: argparse.Namespace) -> int:
    repo = str(Path(args.repo).expanduser().resolve())
    test_cmd = args.test_cmd or os.environ.get("FAS_TEST_CMD")
    workflow = getattr(args, "workflow", None)

    def repair_runner(task: str) -> int:
        old_commit = os.environ.get("FAS_COMMIT")
        old_push = os.environ.get("FAS_PUSH")
        try:
            os.environ["FAS_COMMIT"] = "1"
            os.environ["FAS_PUSH"] = "1"
            argv = ["run", task, "--repo", repo, "--recovery"]
            if test_cmd:
                argv.extend(["--test-cmd", test_cmd])
            return main(argv)
        finally:
            if old_commit is None:
                os.environ.pop("FAS_COMMIT", None)
            else:
                os.environ["FAS_COMMIT"] = old_commit
            if old_push is None:
                os.environ.pop("FAS_PUSH", None)
            else:
                os.environ["FAS_PUSH"] = old_push

    def diagnose_runner(task: str) -> str:
        return _diagnose_scope(repo, task)

    def missing_run_handler(_sha: str) -> None:
        if workflow:
            dispatch_workflow(repo, workflow, args.branch)

    result = watch_and_recover(
        repo,
        max_attempts=args.max_attempts,
        poll_limit=args.poll_limit,
        poll_seconds=args.poll_seconds,
        repair_runner=repair_runner,
        diagnose_runner=diagnose_runner,
        missing_run_handler=missing_run_handler if workflow else None,
    )
    print(result)
    return 0 if result == "success" else 1


def _route_decision(route: dict[str, str]):
    from model_router import Capability, RouteDecision

    return RouteDecision(Capability(route["capability"]), route["model"], route["reason"])


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "init":
        print(init_repository(args.repo))
        return 0
    if args.command == "watch":
        if args.workflow:
            args.branch = subprocess.run(
                ["git", "-C", str(Path(args.repo).expanduser().resolve()), "branch", "--show-current"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            if not args.branch:
                raise ValueError("workflow dispatch requires a named branch")
        return _watch(args)
    return _run_task(args)


if __name__ == "__main__":
    sys.exit(main())
