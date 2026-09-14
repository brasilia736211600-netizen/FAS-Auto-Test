"""Structured final reports for bounded FAS autonomous runs."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fas_git import ensure_fas_excluded

RECOMMENDATIONS = {
    "scope_violation": (
        "The repair proposal exceeded the controller's declared scope. Keep scope enforcement enabled; "
        "inspect the CI evidence and expand scope only when directly justified by concrete repository paths."
    ),
    "scope_unknown": (
        "No concrete repository path could be established from the CI evidence. Inspect the failure and "
        "define a minimal evidence-backed recovery scope before allowing mutation."
    ),
    "push_failed": (
        "The local repair could not be pushed. Verify GitHub authentication and workflow permission scopes "
        "and refresh stale Git credential-cache entries; do not force-push."
    ),
    "repair_failed": (
        "The repair command failed. Inspect the bounded repair output and test failure, then retry only after "
        "the root cause and smallest safe fix are established."
    ),
    "repair_not_pushed": (
        "The repair did not advance the expected commit. Inspect local commit/push state and Git authentication "
        "before another recovery attempt."
    ),
    "non_actionable": (
        "CI was cancelled or timed out. Treat this as non-actionable until the external CI condition is resolved."
    ),
    "poll_limit_exhausted": (
        "The bounded CI polling window expired without a terminal result. Increase the bounded polling window only "
        "after confirming the workflow is actually progressing."
    ),
    "idle_limit_exhausted": (
        "No new remote commit arrived during the idle window. The autonomous loop stopped safely."
    ),
}


def build_report(
    *,
    repository: str,
    branch: str | None,
    initial_sha: str,
    final_sha: str,
    result: str,
    state: dict[str, Any],
) -> dict[str, Any]:
    failure = state.get("failure") or {}
    ci = state.get("ci") or {}
    git = state.get("git") or {}
    test = state.get("test") or {}
    report = {
        "status": "PASS" if result == "success" else "FAIL",
        "repository": repository,
        "branch": branch or git.get("branch"),
        "initial_sha": initial_sha,
        "final_sha": final_sha,
        "result": result,
        "failure": {
            "class": failure.get("class") or (None if result == "success" else result),
            "message": failure.get("message"),
            "stage": failure.get("stage"),
        },
        "ci": {"run_id": ci.get("run_id"), "result": ci.get("result")},
        "test": test,
        "commit": {"sha": git.get("commit_sha")},
        "recommendation": None if result == "success" else RECOMMENDATIONS.get(
            failure.get("class") or result,
            "Inspect the persisted CI failure log and bounded repair output before making another change.",
        ),
        "diagnosis": state.get("diagnosis"),
        "recovery_attempts": state.get("attempt", 0),
        "ci_log": ".fas/logs/ci-failure.log" if (Path(repository) / ".fas" / "logs" / "ci-failure.log").exists() else None,
    }
    return report


def render_report(report: dict[str, Any]) -> str:
    failure = report["failure"]
    ci = report["ci"]
    test = report["test"]
    commit = report["commit"]
    return "\n".join(
        [
            "=== FAS AUTONOMOUS RECOVERY REPORT ===",
            f"STATUS: {report['status']}",
            f"REPOSITORY: {report['repository']}",
            f"BRANCH: {report.get('branch') or 'UNKNOWN'}",
            f"INITIAL_SHA: {report['initial_sha']}",
            f"FINAL_SHA: {report['final_sha']}",
            f"RESULT: {report['result']}",
            f"CI_RUN: {ci.get('run_id') or 'NONE'}",
            f"CI_STATUS: {ci.get('result') or 'UNKNOWN'}",
            "FAILURE:",
            f"  CLASS: {failure.get('class') or 'NONE'}",
            f"  STAGE: {failure.get('stage') or 'UNKNOWN'}",
            f"  MESSAGE: {failure.get('message') or 'NONE'}",
            f"TEST_RESULT: {test.get('result') or 'NOT_RUN'}",
            f"COMMIT: {commit.get('sha') or 'NOT_CREATED'}",
            "RECOMMENDATION:",
            f"  {report.get('recommendation') or 'Task completed successfully.'}",
            f"DIAGNOSIS: {report.get('diagnosis') or 'NONE'}",
            f"RECOVERY_ATTEMPTS: {report.get('recovery_attempts', 0)}",
            f"CI_LOG: {report.get('ci_log') or 'NONE'}",
            "========================================",
        ]
    )


def write_report(repo: str | Path, report: dict[str, Any]) -> Path:
    root = Path(repo).expanduser().resolve()
    ensure_fas_excluded(str(root))
    path = root / ".fas" / "recovery-report.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path
