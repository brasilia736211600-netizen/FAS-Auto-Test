"""Bounded CI watch-and-recovery loop for FAS."""
from __future__ import annotations

import subprocess
import time
from typing import Callable

from fas_github import classify_run, find_run, view_run
from fas_recovery import recover_once


class RecoveryBudgetExceeded(RuntimeError):
    pass


def current_sha(repository: str, *, runner=subprocess.run) -> str:
    result = runner(
        ["git", "-C", repository, "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def watch_and_recover(
    repository: str,
    *,
    max_attempts: int = 3,
    poll_limit: int = 60,
    poll_seconds: float = 5.0,
    runner=subprocess.run,
    repair_runner: Callable[[str], int],
) -> str:
    """Watch the CI run for HEAD and recover actionable failures only."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be positive")
    if poll_limit < 1:
        raise ValueError("poll_limit must be positive")
    sha = current_sha(repository, runner=runner)
    attempts = 0

    for _ in range(poll_limit):
        run = find_run(repository, sha, runner=runner)
        if run is None:
            time.sleep(poll_seconds)
            continue
        outcome = classify_run(run)
        if outcome == "pending":
            time.sleep(poll_seconds)
            continue
        if outcome == "success":
            return "success"
        if outcome != "failure":
            return outcome
        attempts += 1
        if attempts >= max_attempts:
            raise RecoveryBudgetExceeded("CI recovery attempt budget exhausted")
        if recover_once(repository, run.database_id, repair_runner=repair_runner) != 0:
            return "repair_failed"
        return "repaired"

    return "poll_limit_exhausted"
