"""Small, non-destructive Git safety primitives for FAS."""
from __future__ import annotations

import subprocess


FORBIDDEN_GIT_OPERATIONS = {
    "reset --hard",
    "clean",
    "push --force",
    "push -f",
}


def status_porcelain(repo: str) -> str:
    return subprocess.run(
        ["git", "-C", repo, "status", "--porcelain"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def assert_clean(repo: str) -> None:
    status = status_porcelain(repo)
    if status:
        raise RuntimeError("working tree is not clean")


def changed_after(repo: str, before: str) -> bool:
    return status_porcelain(repo) != before


def safe_push(repo: str, *, remote: str = "origin", branch: str | None = None) -> None:
    """Push without force and only from a clean tree.

    The caller must choose the target branch explicitly when it is not the
    currently checked-out branch.
    """
    assert_clean(repo)
    target = branch
    if not target:
        target = subprocess.run(
            ["git", "-C", repo, "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    if not target:
        raise RuntimeError("cannot push from detached HEAD without an explicit branch")
    subprocess.run(["git", "-C", repo, "push", remote, target], check=True)
