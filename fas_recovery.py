"""Autonomous GitHub CI recovery bridge for FAS."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Sequence

from fas_git import ensure_fas_excluded


def failed_logs(
    repository: str,
    run_id: int,
    *,
    runner=subprocess.run,
) -> str:
    result = runner(
        ["gh", "run", "view", str(run_id), "--repo", repository, "--log-failed"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def persist_failure_logs(repo: str | Path, logs: str) -> Path:
    root = Path(repo).expanduser().resolve()
    ensure_fas_excluded(str(root))
    target = root / ".fas" / "logs" / "ci-failure.log"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(logs, encoding="utf-8")
    return target


def build_repair_task(log_path: str | Path) -> str:
    path = Path(log_path)
    return (
        "Repair the current repository using the recorded CI failure. "
        "Read the CI log at {log}. Identify the root cause from fresh evidence, "
        "make the smallest YAGNI-compliant fix, preserve existing behavior and "
        "tests, and run the repository test command before finishing. Do not "
        "reset, clean, force-push, delete unrelated work, or modify secrets."
    ).format(log=path)


def recover_once(
    repository: str,
    run_id: int,
    *,
    repair_runner,
) -> int:
    """Persist CI evidence and delegate one bounded repair attempt."""
    logs = failed_logs(repository, run_id)
    log_path = persist_failure_logs(repository, logs)
    return repair_runner(build_repair_task(log_path))
