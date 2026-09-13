"""Resume a durable FAS task through the canonical FAS runtime."""
from __future__ import annotations

import argparse
from pathlib import Path

from fas_cli import main as fas_main
from fas_runtime import read_state


def build_resume_task(repo: str | Path, task_file: str) -> str:
    root = Path(repo).expanduser().resolve()
    state = read_state(root)
    task_path = Path(task_file)
    if not task_path.is_absolute():
        task_path = root / task_path
    return (
        "RESUME an existing FAS-controlled task from durable repository state. "
        "Do not restart completed work and do not discard existing changes. "
        "First inspect git status, current branch, HEAD, .fas/state.json and the "
        f"task specification at {task_path}. Reconcile completed commits, "
        "in-progress changes, tests and verification evidence. Continue from the "
        "first incomplete execution phase. Follow the task's execution order and "
        "the canonical READ -> VERIFY -> RECONCILE -> PLAN -> EXECUTE -> TEST -> "
        "DIFF -> REVIEW -> COMMIT -> SAVE STATE workflow. Preserve unrelated work. "
        "Use the canonical FAS runner, including model routing, fallback, safety "
        "checks, durable state updates, optional testing, commit and push controls. "
        "Current durable state snapshot: "
        f"phase={state.get('phase')!r}, attempt={state.get('attempt')!r}, "
        f"max_attempts={state.get('max_attempts')!r}, "
        f"commit_sha={state.get('git', {}).get('commit_sha')!r}."
    )


def resume(repo: str | Path, task_file: str) -> int:
    root = Path(repo).expanduser().resolve()
    task = build_resume_task(root, task_file)
    return fas_main(["run", task, "--repo", str(root), "--architecture-impact", "--files-changed", "20"])


def main() -> int:
    parser = argparse.ArgumentParser(prog="fas-resume")
    parser.add_argument("repo", nargs="?", default=".")
    parser.add_argument("task_file", nargs="?", default="docs/FAS_WEBLIBRE_NEXT_BUILD.md")
    args = parser.parse_args()
    return resume(args.repo, args.task_file)


if __name__ == "__main__":
    raise SystemExit(main())
