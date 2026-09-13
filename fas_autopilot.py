"""Persistent autonomous FAS controller for a local Git checkout."""
from __future__ import annotations

import argparse
from pathlib import Path

from fas_cli import _diagnose_scope, _watch
from fas_watch import autopilot as run_autopilot


def run(repo: str | Path, *, max_attempts: int, poll_limit: int, poll_seconds: float, idle_seconds: float, max_cycles: int | None) -> int:
    root = str(Path(repo).expanduser().resolve())
    args = argparse.Namespace(
        repo=root,
        max_attempts=max_attempts,
        poll_limit=poll_limit,
        poll_seconds=poll_seconds,
        test_cmd=None,
    )

    def repair_runner(_task: str) -> int:
        return _watch(args)

    def diagnose_runner(task: str) -> str:
        return _diagnose_scope(root, task)

    result = run_autopilot(
        root,
        max_attempts=max_attempts,
        poll_limit=poll_limit,
        poll_seconds=poll_seconds,
        idle_seconds=idle_seconds,
        max_cycles=max_cycles,
        repair_runner=repair_runner,
        diagnose_runner=diagnose_runner,
    )
    print(result)
    return 0 if result == "success" else 1


def main() -> int:
    parser = argparse.ArgumentParser(prog="fas-autopilot")
    parser.add_argument("repo", nargs="?", default=".")
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--poll-limit", type=int, default=60)
    parser.add_argument("--poll-seconds", type=float, default=5.0)
    parser.add_argument("--idle-seconds", type=float, default=10.0)
    parser.add_argument("--max-cycles", type=int)
    args = parser.parse_args()
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
