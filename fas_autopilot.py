"""Persistent autonomous FAS controller for local or GitHub-first supervision."""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

from fas_cli import _watch
from fas_watch import current_sha


def run(
    repo: str | Path,
    *,
    max_attempts: int,
    poll_limit: int,
    poll_seconds: float,
    idle_seconds: float,
    max_cycles: int | None,
) -> int:
    root = str(Path(repo).expanduser().resolve())
    args = argparse.Namespace(
        repo=root,
        max_attempts=max_attempts,
        poll_limit=poll_limit,
        poll_seconds=poll_seconds,
        test_cmd=None,
    )

    cycles = 0
    while max_cycles is None or cycles < max_cycles:
        result = _watch(args)
        if result != 0:
            return result
        cycles += 1
        if max_cycles is not None and cycles >= max_cycles:
            return 0

        baseline = current_sha(root)
        while current_sha(root) == baseline:
            time.sleep(idle_seconds)

    return 0


def run_github(
    repository: str,
    branch: str,
    *,
    max_attempts: int,
    poll_limit: int,
    poll_seconds: float,
    idle_seconds: float,
    max_cycles: int | None,
    workflow: str | None,
    test_cmd: str | None,
    objective: str | None,
    scope_paths: tuple[str, ...],
) -> int:
    """Supervise a GitHub branch using disposable checkouts only."""
    from fas_remote import RemoteTarget, run_remote
    from fas_report import render_report

    report_path = Path(".fas") / "recovery-report.json"
    old_report_path = os.environ.get("FAS_REMOTE_REPORT_PATH")
    try:
        os.environ["FAS_REMOTE_REPORT_PATH"] = str(report_path.resolve())
        result = run_remote(
            RemoteTarget(repository, branch),
            max_attempts=max_attempts,
            poll_limit=poll_limit,
            poll_seconds=poll_seconds,
            idle_seconds=idle_seconds,
            max_cycles=max_cycles,
            workflow=workflow,
            test_cmd=test_cmd,
            objective=objective,
            scope_paths=scope_paths,
        )
    finally:
        if old_report_path is None:
            os.environ.pop("FAS_REMOTE_REPORT_PATH", None)
        else:
            os.environ["FAS_REMOTE_REPORT_PATH"] = old_report_path

    if report_path.exists():
        report = json.loads(report_path.read_text(encoding="utf-8"))
        print(render_report(report))
    else:
        print(f"FAS RESULT: {result}")
    return 0 if result == "success" else 1


def main() -> int:
    parser = argparse.ArgumentParser(prog="fas-autopilot")
    parser.add_argument("repo", nargs="?", default=".")
    parser.add_argument("--github", help="GitHub OWNER/REPO to supervise without using a local checkout")
    parser.add_argument("--branch", help="GitHub branch for --github mode")
    parser.add_argument("--workflow", help="Optional workflow to dispatch with workflow_dispatch")
    parser.add_argument("--objective-file", help="File containing an explicit mission to execute before CI supervision")
    parser.add_argument("--scope", action="append", default=[], help="Repository-relative path allowed during mission execution; repeat as needed")
    parser.add_argument("--test-cmd")
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--poll-limit", type=int, default=60)
    parser.add_argument("--poll-seconds", type=float, default=5.0)
    parser.add_argument("--idle-seconds", type=float, default=10.0)
    parser.add_argument("--max-cycles", type=int)
    args = parser.parse_args()

    objective = None
    if args.objective_file:
        objective_path = Path(args.objective_file).expanduser().resolve()
        if not objective_path.is_file():
            parser.error(f"objective file not found: {objective_path}")
        objective = objective_path.read_text(encoding="utf-8")
        if not objective.strip():
            parser.error("objective file must not be empty")

    if args.github:
        if not args.branch:
            parser.error("--branch is required with --github")
        if objective and not args.scope:
            parser.error("--scope is required with --objective-file")
        return run_github(
            args.github,
            args.branch,
            max_attempts=args.max_attempts,
            poll_limit=args.poll_limit,
            poll_seconds=args.poll_seconds,
            idle_seconds=args.idle_seconds,
            max_cycles=args.max_cycles,
            workflow=args.workflow,
            test_cmd=args.test_cmd,
            objective=objective,
            scope_paths=tuple(args.scope),
        )

    if args.objective_file or args.scope:
        parser.error("--objective-file and --scope require --github mode")
    if args.test_cmd:
        parser.error("--test-cmd is only supported with --github mode")
    return run(
        args.repo,
        max_attempts=args.max_attempts,
        poll_limit=args.poll_limit,
        poll_seconds=args.poll_seconds,
        idle_seconds=args.idle_seconds,
        max_cycles=args.max_cycles,
    )


if __name__ == "__main__":
    raise SystemExit(main())
