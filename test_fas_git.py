import subprocess

import pytest

from fas_git import assert_clean, changed_after, commit_if_changed, safe_push, status_porcelain


def _run_status(monkeypatch, output=""):
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda command, **kwargs: subprocess.CompletedProcess(command, 0, output, ""),
    )


def test_status_porcelain_reads_machine_git_state(monkeypatch):
    _run_status(monkeypatch, " M file.py\n")
    assert status_porcelain(".") == " M file.py\n"


def test_assert_clean_rejects_changes(monkeypatch):
    _run_status(monkeypatch, " M file.py\n")
    with pytest.raises(RuntimeError, match="not clean"):
        assert_clean(".")


def test_changed_after_detects_new_changes(monkeypatch):
    _run_status(monkeypatch, " M file.py\n")
    assert changed_after(".", "") is True


def test_safe_push_never_uses_force(monkeypatch):
    calls = []

    def fake_run(command, **kwargs):
        calls.append(command)
        if command[-2:] == ["branch", "--show-current"]:
            return subprocess.CompletedProcess(command, 0, "main\n", "")
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(subprocess, "run", fake_run)
    safe_push(".")
    push = calls[-1]
    assert "--force" not in push
    assert "-f" not in push
    assert push[-2:] == ["origin", "main"]


def test_commit_if_changed_does_nothing_on_clean_tree(monkeypatch):
    calls = []

    def fake_run(command, **kwargs):
        calls.append(command)
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(subprocess, "run", fake_run)
    assert commit_if_changed(".", "test commit") is None
    assert len(calls) == 1


def test_commit_if_changed_uses_normal_commit(monkeypatch):
    calls = []
    responses = iter([
        subprocess.CompletedProcess(["git"], 0, " M file.py\n", ""),
        subprocess.CompletedProcess(["git"], 0, "", ""),
        subprocess.CompletedProcess(["git"], 0, "", ""),
        subprocess.CompletedProcess(["git"], 0, "abc123\n", ""),
    ])

    def fake_run(command, **kwargs):
        calls.append(command)
        return next(responses)

    monkeypatch.setattr(subprocess, "run", fake_run)
    assert commit_if_changed(".", "feat: test") == "abc123"
    assert calls[1][-2:] == ["add", "-A"]
    assert calls[2][4:6] == ["commit", "-m"]
    assert "--force" not in calls[2]
