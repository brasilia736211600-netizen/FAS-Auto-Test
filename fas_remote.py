"""GitHub-first autonomous supervision using disposable remote checkouts."""
from __future__ import annotations

import os
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from fas_cli import _watch


@dataclass(frozen=True)
class RemoteTarget:
    repository: str
    branch: str


def _run(command: list[str], *, runner=subprocess.run) -> subprocess.CompletedProcess[str]:
    return runner(command, check=True, capture_output=True, text=True)


def remote_head(
    repository: str,
    branch: str,
    *,
    runner=subprocess.run,
) -> str:
    """Resolve a branch HEAD directly from GitHub, without a local checkout."""
    result = _run(
        [
            "git",
            "ls-remote",
            f"https://github.com/{repository}.git",
            f"refs/heads/{branch}",
        ],
        runner=runner,
    )
    line = result.stdout.strip().splitlines()
    if not line:
        raise RuntimeError(f"GitHub branch not found: {repository}@{branch}")
    sha = line[0].split()[0]
    if len(sha) != 40:
        raise RuntimeError(f"invalid GitHub branch SHA: {sha}")
    return sha


def clone_remote(
    target: RemoteTarget,
    destination: Path,
    *,
    runner=subprocess.run,
) -> None:
    """Create a disposable checkout of exactly the requested GitHub branch."""
    _run(
        [
            "git",
            "clone",
            "--branch",
            target.branch,
            "--single-branch",
            f"https://github.com/{target.repository}.git",
            str(destination),
        ],
        runner=runner,
    )


def wait_for_remote_change(
    target: RemoteTarget,
    previous_sha: str,
    *,
    poll_seconds: float = 10.0,
    poll_limit: int | None = None,
    runner=subprocess.run,
) -> str | None:
    """Wait for GitHub branch HEAD to advance beyond the observed SHA."""
    polls = 0
    while poll_limit is None or polls < poll_limit:
        polls += 1
        sha = remote_head(target.repository, target.branch, runner=runner)
        if sha != previous_sha:
            return sha
        time.sleep(poll_seconds)
    return None


def _run_clean_watch(
    target: RemoteTarget,
    *,
    poll_limit: int,
    poll_seconds: float,
    workflow: str | None,
    test_cmd: str | None,
    runner,
    watch_runner,
    retry_context: str | None,
) -> tuple[int, str]:
    """Run one recovery attempt inside a fresh disposable checkout."""
    with tempfile.TemporaryDirectory(prefix="fas-remote-") as temp_root:
        checkout = Path(temp_root) / "repo"
        clone_remote(target, checkout, runner=runner)

        args = type(
            "RemoteWatchArgs",
            (),
            {
                "repo": str(checkout),
                "max_attempts": 1,
                "poll_limit": poll_limit,
                "poll_seconds": poll_seconds,
                "test_cmd": test_cmd,
                "workflow": workflow,
                "branch": target.branch,
            },
        )()
        watcher = watch_runner or _watch
        old_repository = os.environ.get("FAS_REPORT_REPOSITORY")
        old_branch = os.environ.get("FAS_REPORT_BRANCH")
        old_retry = os.environ.get("FAS_RETRY_CONTEXT")
        try:
            os.environ["FAS_REPORT_REPOSITORY"] = target.repository
            os.environ["FAS_REPORT_BRANCH"] = target.branch
            if retry_context:
                os.environ["FAS_RETRY_CONTEXT"] = retry_context
            else:
                os.environ.pop("FAS_RETRY_CONTEXT", None)
            result = watcher(args)
            return result, str(checkout)
        finally:
            if old_repository is None:
                os.environ.pop("FAS_REPORT_REPOSITORY", None)
            else:
                os.environ["FAS_REPORT_REPOSITORY"] = old_repository
            if old_branch is None:
                os.environ.pop("FAS_REPORT_BRANCH", None)
            else:
                os.environ["FAS_REPORT_BRANCH"] = old_branch
            if old_retry is None:
                os.environ.pop("FAS_RETRY_CONTEXT", None)
            else:
                os.environ["FAS_RETRY_CONTEXT"] = old_retry


def run_remote(
    target: RemoteTarget,
    *,
    max_attempts: int = 3,
    poll_limit: int = 60,
    poll_seconds: float = 5.0,
    idle_seconds: float = 10.0,
    max_cycles: int | None = None,
    workflow: str | None = None,
    test_cmd: str | None = None,
    runner=subprocess.run,
    watch_runner: Callable[[object], int] | None = None,
) -> str:
    """Run FAS against GitHub using clean disposable retries and clean-branch monitoring."""
    if max_cycles is not None and max_cycles < 1:
        raise ValueError("max_cycles must be positive when provided")
    if max_attempts < 1 or poll_limit < 1:
        raise ValueError("max_attempts and poll_limit must be positive")
    if idle_seconds < 0:
        raise ValueError("idle_seconds must not be negative")

    cycles = 0
    while max_cycles is None or cycles < max_cycles:
        baseline = remote_head(target.repository, target.branch, runner=runner)
        retry_context = None
        last_result = 1

        for attempt in range(1, max_attempts + 1):
            result, _checkout = _run_clean_watch(
                target,
                poll_limit=poll_limit,
                poll_seconds=poll_seconds,
                workflow=workflow,
                test_cmd=test_cmd,
                runner=runner,
                watch_runner=watch_runner,
                retry_context=retry_context,
            )
            last_result = result
            if result == 0:
                break
            retry_context = (
                f"Recovery attempt {attempt} was rejected with result code {result}. "
                "Use a fresh checkout, re-read the CI evidence, and choose a different "
                "minimal repair rather than repeating the rejected change."
            )

        if last_result != 0:
            return "remote_watch_failed"

        cycles += 1
        if max_cycles is not None and cycles >= max_cycles:
            return "success"

        next_sha = wait_for_remote_change(
            target,
            baseline,
            poll_seconds=idle_seconds,
            runner=runner,
        )
        if next_sha is None:
            return "remote_idle_limit_exhausted"

    return "success"
