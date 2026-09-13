import json
import subprocess

import pytest

from fas_github import WorkflowRun, classify_run, find_run, resolve_repository, view_run


def _runner_with(payload):
    def runner(command, **kwargs):
        return subprocess.CompletedProcess(command, 0, json.dumps(payload), "")

    return runner


def test_resolve_repository_preserves_owner_repo():
    assert resolve_repository("owner/repo") == "owner/repo"


def test_resolve_repository_from_https_origin(tmp_path):
    commands = []

    def runner(command, **kwargs):
        commands.append(command)
        return subprocess.CompletedProcess(
            command,
            0,
            "https://github.com/brasilia736211600-netizen/FAS-Auto-Test.git\n",
            "",
        )

    assert resolve_repository(str(tmp_path), runner=runner) == (
        "brasilia736211600-netizen/FAS-Auto-Test"
    )
    assert commands == [
        ["git", "-C", str(tmp_path.resolve()), "remote", "get-url", "origin"]
    ]


def test_resolve_repository_from_ssh_origin(tmp_path):
    def runner(command, **kwargs):
        return subprocess.CompletedProcess(
            command,
            0,
            "git@github.com:brasilia736211600-netizen/FAS-Auto-Test.git\n",
            "",
        )

    assert resolve_repository(str(tmp_path), runner=runner) == (
        "brasilia736211600-netizen/FAS-Auto-Test"
    )


def test_resolve_repository_rejects_non_github_origin(tmp_path):
    def runner(command, **kwargs):
        return subprocess.CompletedProcess(
            command, 0, "https://gitlab.com/example/repo.git\n", ""
        )

    with pytest.raises(ValueError, match="not a GitHub repository"):
        resolve_repository(str(tmp_path), runner=runner)


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
