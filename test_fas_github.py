import json
import subprocess

from fas_github import WorkflowRun, classify_run, find_run, view_run


def _runner_with(payload):
    def runner(command, **kwargs):
        return subprocess.CompletedProcess(command, 0, json.dumps(payload), "")

    return runner


def test_find_run_matches_commit_sha():
    payload = [
        {
            "databaseId": 12,
            "status": "completed",
            "conclusion": "success",
            "headSha": "abc",
            "workflowName": "FAS CI",
        }
    ]
    run = find_run("owner/repo", "abc", runner=_runner_with(payload))
    assert run == WorkflowRun(12, "completed", "success", "abc", "FAS CI")


def test_find_run_returns_none_for_missing_commit():
    assert find_run("owner/repo", "abc", runner=_runner_with([])) is None


def test_view_run_parses_machine_payload():
    payload = {
        "databaseId": 8,
        "status": "in_progress",
        "conclusion": None,
        "headSha": "def",
        "workflowName": "FAS CI",
    }
    run = view_run("owner/repo", 8, runner=_runner_with(payload))
    assert classify_run(run) == "pending"


def test_classify_terminal_states():
    assert classify_run(WorkflowRun(1, "completed", "success", "a", "ci")) == "success"
    assert classify_run(WorkflowRun(2, "completed", "failure", "a", "ci")) == "failure"
    assert classify_run(WorkflowRun(3, "completed", "timed_out", "a", "ci")) == "non_actionable"
