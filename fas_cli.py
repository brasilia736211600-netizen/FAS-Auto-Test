"""Minimal portable command-line entry point for FAS."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

from fas_runtime import init_repository, read_state, record_test, select_route, write_state
from model_router import TaskSignals


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
    model = os.environ.get("FAS_MODEL", planned_route["model"])

    start = time.monotonic()
    completed = subprocess.run(
        ["opencode", "run", "--auto", "--model", model, "--agent", "build", args.task],
        cwd=repo,
        check=False,
    )
    duration = time.monotonic() - start
    if completed.returncode != 0:
        record_test(repo, "opencode run", f"FAIL:{completed.returncode}", duration)
        return completed.returncode

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

    state = read_state(repo)
    state["phase"] = "EXECUTE"
    state["attempt"] = max(1, state.get("attempt", 0))
    state["route"] = dict(planned_route)
    state["route"]["effective_model"] = model
    write_state(repo, state)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "init":
        print(init_repository(args.repo))
        return 0
    return _run_task(args)


if __name__ == "__main__":
    sys.exit(main())
