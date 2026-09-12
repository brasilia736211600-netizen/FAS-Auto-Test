"""Minimal portable command-line entry point for FAS."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

from fas_fallback import candidate_models, run_with_fallback
from fas_git import changed_after, status_porcelain
from fas_runtime import init_repository, read_state, record_test, select_route, write_state
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
    return parser


def _run_task(args: argparse.Namespace) -> int:
    repo = Path(args.repo).expanduser().resolve()
    state = read_state(repo)
    if state.get("repository") != str(repo):
        init_repository(repo)

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
    candidates = tuple(dict.fromkeys(((override,) if override else ()) + candidate_models(_route_decision(planned_route), configured)))
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
    return 0


def _route_decision(route: dict[str, str]):
    from model_router import Capability, RouteDecision

    return RouteDecision(Capability(route["capability"]), route["model"], route["reason"])


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "init":
        print(init_repository(args.repo))
        return 0
    return _run_task(args)


if __name__ == "__main__":
    sys.exit(main())