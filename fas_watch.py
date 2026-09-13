"""CI watch, bounded recovery, and continuous autonomous supervision for FAS."""
from __future__ import annotations

import subprocess
import time
from typing import Callable

from fas_github import classify_run, find_run
from fas_git import PUSH_FAILED_CODE, SCOPE_VIOLATION_CODE
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
    diagnose_runner: Callable[[str], str] | None = None,
) -> str:
    """Watch CI and perform bounded recovery until PASS or a stop condition."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be positive")
    if poll_limit < 1:
        raise ValueError("poll_limit must be positive")

    sha = current_sha(repository, runner=runner)
    attempts = 0
    polls = 0

    while polls < poll_limit:
        polls += 1
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
        if attempts > max_attempts:
            raise RecoveryBudgetExceeded("CI recovery attempt budget exhausted")

        recovery_kwargs = {"repair_runner": repair_runner}
        if diagnose_runner is not None:
            recovery_kwargs["diagnose_runner"] = diagnose_runner
        repair_result = recover_once(repository, run.database_id, **recovery_kwargs)
        if repair_result == SCOPE_VIOLATION_CODE:
            return "scope_violation"
        if repair_result == PUSH_FAILED_CODE:
            return "push_failed"
        if repair_result != 0:
            return "repair_failed"

        # A successful repair must produce a new commit/push before we watch
        # again. Refresh HEAD so the next lookup cannot accept the old failed run.
        new_sha = current_sha(repository, runner=runner)
        if new_sha == sha:
            return "repair_not_pushed"
        sha = new_sha

    return "poll_limit_exhausted"


def wait_for_new_sha(
    repository: str,
    previous_sha: str,
    *,
    poll_seconds: float = 5.0,
    runner=subprocess.run,
    poll_limit: int | None = None,
) -> str | None:
    """Wait until the local checkout advances to a new commit."""
    polls = 0
    while poll_limit is None or polls < poll_limit:
        polls += 1
        sha = current_sha(repository, runner=runner)
        if sha != previous_sha:
            return sha
        time.sleep(poll_seconds)
    return None


def autopilot(
    repository: str,
    *,
    max_attempts: int = 3,
    poll_limit: int = 60,
    poll_seconds: float = 5.0,
    idle_seconds: float = 10.0,
    max_cycles: int | None = None,
    runner=subprocess.run,
    repair_runner: Callable[[str], int],
    diagnose_runner: Callable[[str], str] | None = None,
) -> str:
    """Continuously supervise HEAD, recover failures, then wait for the next commit."""
    if idle_seconds < 0:
        raise ValueError("idle_seconds must not be negative")
    if max_cycles is not None and max_cycles < 1:
        raise ValueError("max_cycles must be positive when provided")

    cycles = 0
    while max_cycles is None or cycles < max_cycles:
        result = watch_and_recover(
            repository,
            max_attempts=max_attempts,
            poll_limit=poll_limit,
            poll_seconds=poll_seconds,
            runner=runner,
            repair_runner=repair_runner,
            diagnose_runner=diagnose_runner,
        )
        cycles += 1
        if result != "success":
            return result
        if max_cycles is not None and cycles >= max_cycles:
            return "success"

        baseline = current_sha(repository, runner=runner)
        next_sha = wait_for_new_sha(
            repository,
            baseline,
            poll_seconds=idle_seconds,
            runner=runner,
        )
        if next_sha is None:
            return "idle_limit_exhausted"

    return "success"
