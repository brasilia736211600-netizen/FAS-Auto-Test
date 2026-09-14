"""GitHub-first autonomous supervision using disposable remote checkouts."""
from __future__ import annotations

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
    """Run FAS against GitHub using only disposable temporary checkouts."""
    if max_cycles is not None and max_cycles < 1:
        raise ValueError("max_cycles must be positive when provided")
    if max_attempts < 1 or poll_limit < 1:
        raise ValueError("max_attempts and poll_limit must be positive")
    if idle_seconds < 0:
        raise ValueError("idle_seconds must not be negative")

    cycles = 0
    while max_cycles is None or cycles < max_cycles:
        baseline = remote_head(target.repository, target.branch, runner=runner)
        with tempfile.TemporaryDirectory(prefix="fas-remote-") as temp_root:
            checkout = Path(temp_root) / "repo"
            clone_remote(target, checkout, runner=runner)

            args = type(
                "RemoteWatchArgs",
                (),
                {
                    "repo": str(checkout),
                    "max_attempts": max_attempts,
                    "poll_limit": poll_limit,
                    "poll_seconds": poll_seconds,
                    "test_cmd": test_cmd,
                    "workflow": workflow,
                    "branch": target.branch,
                },
            )()
            watcher = watch_runner or _watch
            result = watcher(args)
            if result != 0:
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
