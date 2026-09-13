"""Persistent autonomous FAS controller for a local Git checkout."""
from __future__ import annotations

import argparse
import time
from pathlib import Path

from fas_cli import _watch
from fas_watch import current_sha


def run(repo: str | Path, *, max_attempts: int, poll_limit: int, poll_seconds: float, idle_seconds: float, max_cycles: int | None) -> int:
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
