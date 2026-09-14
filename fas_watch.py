"""CI watch, bounded recovery, and continuous autonomous supervision for FAS."""
from __future__ import annotations

import subprocess
import time
from typing import Callable

from fas_github import classify_run, find_run
from fas_git import PUSH_FAILED_CODE, SCOPE_VIOLATION_CODE
from fas_recovery import recover_once
from fas_runtime import read_state, write_state


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


def _record_ci(repository: str, run_id: int, result: str) -> None:
    state = read_state(repository)
    state["ci"] = {"run_id": run_id, "result": result}
    write_state(repository, state)


def _record_failure(repository: str, failure_class: str, stage: str, message: str | None = None) -> None:
    state = read_state(repository)
    state["failure"] = {
        "class": failure_class,
        "stage": stage,
        "message": message,
    }
    write_state(repository, state)


def watch_and_recover(
    repository: str,
    *,
    max_attempts: int = 3,
    poll_limit: int = 60,
    poll_seconds: float = 5.0,
    runner=subprocess.run,
    repair_runner: Callable[[str], int],
    diagnose_runner: Callable[[str], str] | None = None,
    missing_run_handler: Callable[[str], None] | None = None,
) -> str:
    """Watch CI and perform bounded recovery until PASS or a stop condition."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be positive")
    if poll_limit < 1:
        raise ValueError("poll_limit must be positive")

    sha = current_sha(repository, runner=runner)
    attempts = 0
    polls = 0
    dispatched_sha: str | None = None

    while polls < poll_limit:
        polls += 1
        run = find_run(repository, sha, runner=runner)
        if run is None:
            if missing_run_handler is not None and dispatched_sha != sha:
                missing_run_handler(sha)
                dispatched_sha = sha
            time.sleep(poll_seconds)
            continue

        dispatched_sha = None
        outcome = classify_run(run)
        _record_ci(repository, run.database_id, outcome)
        if outcome == "pending":
            time.sleep(poll_seconds)
            continue
        if outcome == "success":
            return "success"
        if outcome != "failure":
            _record_failure(repository, outcome, "CI", f"GitHub CI ended with {outcome}")
            return outcome

        attempts += 1
        if attempts > max_attempts:
            message = "CI recovery attempt budget exhausted"
            _record_failure(repository, "recovery_budget_exhausted", "RECOVERY", message)
            raise RecoveryBudgetExceeded(message)

        recovery_kwargs = {"repair_runner": repair_runner}
        if diagnose_runner is not None:
            recovery_kwargs["diagnose_runner"] = diagnose_runner
        repair_result = recover_once(repository, run.database_id, **recovery_kwargs)
        if repair_result == SCOPE_VIOLATION_CODE:
            _record_failure(repository, "scope_violation", "RECOVERY / SCOPE VALIDATION", "Repair changed a path outside the declared recovery scope.")
            return "scope_violation"
        if repair_result == PUSH_FAILED_CODE:
            _record_failure(repository, "push_failed", "RECOVERY / PUSH", "The repaired checkout could not be pushed to GitHub.")
            return "push_failed"
        if repair_result != 0:
            _record_failure(repository, "repair_failed", "RECOVERY / REPAIR OR TEST", f"Repair command returned exit code {repair_result}.")
            return "repair_failed"

        new_sha = current_sha(repository, runner=runner)
        if new_sha == sha:
            _record_failure(repository, "repair_not_pushed", "RECOVERY / COMMIT-PUSH", "The repair completed but HEAD did not advance to a new commit.")
            return "repair_not_pushed"
        sha = new_sha
        dispatched_sha = None

    _record_failure(repository, "poll_limit_exhausted", "CI WATCH", "The bounded polling window expired before CI reached a terminal actionable result.")
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
            _record_failure(repository, "idle_limit_exhausted", "AUTOPILOT IDLE", "No new commit arrived during the idle window.")
            return "idle_limit_exhausted"

    return "success"
