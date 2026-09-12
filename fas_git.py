"""Small, non-destructive Git safety primitives for FAS."""
from __future__ import annotations

import subprocess
from pathlib import Path

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


def ensure_fas_excluded(repo: str) -> None:
    """Keep FAS operational state local without changing tracked project files."""
    root = Path(repo).resolve()
    git_dir = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--git-dir"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    git_path = Path(git_dir)
    if not git_path.is_absolute():
        git_path = root / git_path
    exclude = git_path / "info" / "exclude"
    exclude.parent.mkdir(parents=True, exist_ok=True)
    marker = ".fas/"
    existing = exclude.read_text(encoding="utf-8") if exclude.exists() else ""
    lines = {line.strip() for line in existing.splitlines() if line.strip()}
    if marker not in lines:
        prefix = "" if not existing or existing.endswith("\n") else "\n"
        exclude.write_text(existing + prefix + marker + "\n", encoding="utf-8")


def commit_if_changed(repo: str, message: str) -> str | None:
    """Create a normal commit only when project files changed."""
    current = status_porcelain(repo)
    if not current:
        return None
    subprocess.run(["git", "-C", repo, "add", "-A"], check=True)
    subprocess.run(["git", "-C", repo, "commit", "-m", message], check=True)
    return subprocess.run(
        ["git", "-C", repo, "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def safe_push(repo: str, *, remote: str = "origin", branch: str | None = None) -> None:
    """Push without force and only from a clean tree."""
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
