"""Persistent autonomous FAS controller for local or GitHub-first supervision."""
from __future__ import annotations

import argparse
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
) -> int:
    """Supervise a GitHub branch using disposable checkouts only."""
    from fas_remote import RemoteTarget, run_remote

    result = run_remote(
        RemoteTarget(repository, branch),
        max_attempts=max_attempts,
        poll_limit=poll_limit,
        poll_seconds=poll_seconds,
        idle_seconds=idle_seconds,
        max_cycles=max_cycles,
        workflow=workflow,
        test_cmd=test_cmd,
    )
    print(result)
    return 0 if result == "success" else 1


def main() -> int:
    parser = argparse.ArgumentParser(prog="fas-autopilot")
    parser.add_argument("repo", nargs="?", default=".")
    parser.add_argument("--github", help="GitHub OWNER/REPO to supervise without using a local checkout")
    parser.add_argument("--branch", help="GitHub branch for --github mode")
    parser.add_argument("--workflow", help="Optional workflow to dispatch with workflow_dispatch")
    parser.add_argument("--test-cmd")
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--poll-limit", type=int, default=60)
    parser.add_argument("--poll-seconds", type=float, default=5.0)
    parser.add_argument("--idle-seconds", type=float, default=10.0)
    parser.add_argument("--max-cycles", type=int)
    args = parser.parse_args()

    if args.github:
        if not args.branch:
            parser.error("--branch is required with --github")
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
        )

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
