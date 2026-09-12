"""Minimal GitHub Actions bridge for FAS running on Termux/Linux."""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class WorkflowRun:
    database_id: int
    status: str
    conclusion: str | None
    head_sha: str
    workflow_name: str


def _run_json(
    command: Sequence[str],
    *,
    runner=subprocess.run,
) -> object:
    completed = runner(command, check=True, capture_output=True, text=True)
    return json.loads(completed.stdout)


def find_run(
    repository: str,
    sha: str,
    *,
    runner=subprocess.run,
) -> WorkflowRun | None:
    """Find the newest GitHub Actions run for a pushed commit."""
    data = _run_json(
        [
            "gh",
            "run",
            "list",
            "--repo",
            repository,
            "--commit",
            sha,
            "--json",
            "databaseId,status,conclusion,headSha,workflowName",
            "--limit",
            "10",
        ],
        runner=runner,
    )
    if not isinstance(data, list):
        raise ValueError("gh returned an invalid workflow run payload")
    for item in data:
        if item.get("headSha") == sha:
            return WorkflowRun(
                database_id=int(item["databaseId"]),
                status=str(item["status"]),
                conclusion=item.get("conclusion"),
                head_sha=str(item["headSha"]),
                workflow_name=str(item["workflowName"]),
            )
    return None


def view_run(
    repository: str,
    run_id: int,
    *,
    runner=subprocess.run,
) -> WorkflowRun:
    data = _run_json(
        [
            "gh",
            "run",
            "view",
            str(run_id),
            "--repo",
            repository,
            "--json",
            "databaseId,status,conclusion,headSha,workflowName",
        ],
        runner=runner,
    )
    return WorkflowRun(
        database_id=int(data["databaseId"]),
        status=str(data["status"]),
        conclusion=data.get("conclusion"),
        head_sha=str(data["headSha"]),
        workflow_name=str(data["workflowName"]),
    )


def classify_run(run: WorkflowRun) -> str:
    if run.status in {"queued", "in_progress"}:
        return "pending"
    if run.conclusion == "success":
        return "success"
    if run.conclusion == "failure":
        return "failure"
    if run.conclusion in {"cancelled", "timed_out"}:
        return "non_actionable"
    return "unknown"
