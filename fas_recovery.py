"""Autonomous GitHub CI recovery bridge for FAS."""
from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

from fas_git import ensure_fas_excluded
from fas_github import resolve_repository

_FAILED_PATH = re.compile(r"\bFAILED\s+([^\s:]+)(?:::|$)")
_TRACE_PATH = re.compile(r'\bFile "([^"]+)"')
_EXISTING_PATH = re.compile(r"(?<![\w./-])([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*\.[A-Za-z0-9_.-]+)")


def failed_logs(repository: str, run_id: int, *, runner=subprocess.run) -> str:
    repository = resolve_repository(repository, runner=runner)
    result = runner(["gh", "run", "view", str(run_id), "--repo", repository, "--log-failed"], check=True, capture_output=True, text=True)
    return result.stdout


def workflow_file(repository: str | Path, run_id: int, *, runner=subprocess.run) -> str | None:
    """Resolve the failed run's workflow definition to a local workflow file."""
    root = Path(repository).expanduser().resolve()
    try:
        repo_name = resolve_repository(str(root), runner=runner)
        result = runner(["gh", "run", "view", str(run_id), "--repo", repo_name, "--json", "workflowName"], check=True, capture_output=True, text=True)
        workflow_name = str(json.loads(result.stdout).get("workflowName", "")).strip()
    except (subprocess.CalledProcessError, ValueError, json.JSONDecodeError):
        return None
    if not workflow_name:
        return None
    candidates = []
    for path in (root / ".github" / "workflows").glob("*.y*ml"):
        text = path.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            if line.strip().startswith("name:"):
                name = line.split(":", 1)[1].strip().strip("'\"")
                if name == workflow_name:
                    candidates.append(path)
                    break
    if len(candidates) != 1:
        return None
    return candidates[0].relative_to(root).as_posix()


def persist_failure_logs(repo: str | Path, logs: str) -> Path:
    root = Path(repo).expanduser().resolve()
    ensure_fas_excluded(str(root))
    target = root / ".fas" / "logs" / "ci-failure.log"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(logs, encoding="utf-8")
    return target


def _resolve_evidence_path(repo: Path, raw_path: str) -> Path | None:
    candidate = Path(raw_path.strip().strip("`'\""))
    if candidate.is_absolute():
        try:
            candidate.relative_to(repo)
        except ValueError:
            return None
        return candidate
    direct = repo / candidate
    if direct.exists() and ".git" not in direct.parts and ".fas" not in direct.parts:
        return direct
    matches = [path for path in repo.rglob(candidate.name) if path.is_file() and ".git" not in path.parts and ".fas" not in path.parts]
    return matches[0] if len(matches) == 1 else None


def recovery_scope(repo: str | Path, logs: str) -> tuple[str, ...]:
    """Infer a conservative file/directory scope from concrete CI paths."""
    root = Path(repo).expanduser().resolve()
    raw_paths = _FAILED_PATH.findall(logs) + _TRACE_PATH.findall(logs) + _EXISTING_PATH.findall(logs)
    resolved = []
    for raw in raw_paths:
        path = _resolve_evidence_path(root, raw)
        if path is not None:
            resolved.append(path)
    unique = []
    seen = set()
    for path in resolved:
        relative = path.relative_to(root).as_posix()
        scope = relative if path.parent == root else f"{path.parent.relative_to(root).as_posix()}/"
        if scope not in seen:
            unique.append(scope)
            seen.add(scope)
    return tuple(unique)


def build_scope_diagnosis_task(log_path: str | Path) -> str:
    return (
        "Diagnose the recorded CI failure without changing any repository files. "
        "Read {log}, inspect the current repository, and identify the smallest set "
        "of repository-relative files or directories directly implicated by the failure. "
        "Output ONLY one path per line, with no prose, markdown, or code fences. "
        "Every path must exist in the repository. Do not include .git or .fas paths."
    ).format(log=Path(log_path))


def diagnosed_scope(repo: str | Path, output: str) -> tuple[str, ...]:
    """Validate model-proposed recovery scope before permitting mutation."""
    root = Path(repo).expanduser().resolve()
    scopes = []
    seen = set()
    for line in output.splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#"):
            continue
        path = _resolve_evidence_path(root, raw)
        if path is None:
            continue
        relative = path.relative_to(root).as_posix()
        scope = relative if path.is_file() or path.parent == root else f"{relative.rstrip('/')}/"
        if scope not in seen:
            scopes.append(scope)
            seen.add(scope)
    return tuple(scopes)


def build_repair_task(log_path: str | Path, allowed_paths: tuple[str, ...] = ()) -> str:
    path = Path(log_path)
    scope_text = ", ".join(allowed_paths) if allowed_paths else "UNKNOWN"
    return (
        "Repair the current repository using the recorded CI failure. "
        "Read the CI log at {log}. Identify the root cause from fresh evidence, "
        "make the smallest YAGNI-compliant fix, preserve existing behavior and "
        "tests, and run the repository test command before finishing. The declared "
        "recovery scope is: {scope}. If the failure is in CI orchestration/configuration, "
        "the workflow file in scope is eligible; otherwise prefer the concrete source/test "
        "path from the failure evidence. Do not modify files outside that scope unless "
        "the scope is explicitly expanded by the controller. Do not reset, clean, "
        "force-push, delete unrelated work, or modify secrets."
    ).format(log=path, scope=scope_text)


def recover_once(repository: str, run_id: int, *, repair_runner, diagnose_runner=None) -> int:
    """Persist CI evidence and delegate one bounded repair attempt."""
    logs = failed_logs(repository, run_id)
    log_path = persist_failure_logs(repository, logs)
    allowed_paths = list(recovery_scope(repository, logs))
    workflow = workflow_file(repository, run_id)
    if workflow and workflow not in allowed_paths:
        allowed_paths.append(workflow)
    if diagnose_runner is not None:
        diagnosis = diagnose_runner(build_scope_diagnosis_task(log_path))
        for path in diagnosed_scope(repository, diagnosis):
            if path not in allowed_paths:
                allowed_paths.append(path)
    if not allowed_paths:
        return 77
    scope = tuple(allowed_paths)
    old_scope = os.environ.get("FAS_ALLOWED_PATHS")
    old_message = os.environ.get("FAS_COMMIT_MESSAGE")
    try:
        os.environ["FAS_ALLOWED_PATHS"] = "\n".join(scope)
        os.environ["FAS_COMMIT_MESSAGE"] = "fix: autonomous CI recovery"
        return repair_runner(build_repair_task(log_path, scope))
    finally:
        if old_scope is None:
            os.environ.pop("FAS_ALLOWED_PATHS", None)
        else:
            os.environ["FAS_ALLOWED_PATHS"] = old_scope
        if old_message is None:
            os.environ.pop("FAS_COMMIT_MESSAGE", None)
        else:
            os.environ["FAS_COMMIT_MESSAGE"] = old_message
