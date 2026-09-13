"""Resume a durable FAS task from repository state."""
from __future__ import annotations

import subprocess
from pathlib import Path

from fas_runtime import read_state


def build_resume_task(repo: str | Path, task_file: str) -> str:
    root = Path(repo).expanduser().resolve()
    state = read_state(root)
    return (
        "RESUME an existing FAS-controlled task from durable repository state. "
        "Do not restart completed work and do not discard existing changes. "
        "First inspect git status, current branch, HEAD, .fas/state.json and the "
        f"task specification at {Path(task_file)}. Reconcile completed commits, "
        "in-progress changes, tests and verification evidence. Continue from the "
        "first incomplete execution phase. Follow the task's execution order and "
        "the canonical READ -> VERIFY -> RECONCILE -> PLAN -> EXECUTE -> TEST -> "
        "DIFF -> REVIEW -> COMMIT -> SAVE STATE workflow. Preserve unrelated work. "
        "Current durable state snapshot: "
        f"phase={state.get('phase')!r}, attempt={state.get('attempt')!r}, "
        f"max_attempts={state.get('max_attempts')!r}, "
        f"commit_sha={state.get('git', {}).get('commit_sha')!r}."
    )


def resume(repo: str | Path, task_file: str) -> int:
    root = Path(repo).expanduser().resolve()
    task = build_resume_task(root, task_file)
    completed = subprocess.run(
        ["opencode", "run", "--auto", "--agent", "build", task],
        cwd=root,
        check=False,
    )
    return completed.returncode


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog="fas-resume")
    parser.add_argument("repo", nargs="?", default=".")
    parser.add_argument("task_file", nargs="?", default="docs/FAS_WEBLIBRE_NEXT_BUILD.md")
    raise SystemExit(resume(parser.parse_args().repo, parser.parse_args().task_file))
