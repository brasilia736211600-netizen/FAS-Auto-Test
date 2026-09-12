import subprocess

import pytest

from fas_github import WorkflowRun
from fas_watch import RecoveryBudgetExceeded, watch_and_recover


def test_watch_returns_success_for_completed_run(monkeypatch):
    monkeypatch.setattr("fas_watch.current_sha", lambda repository, runner=None: "abc")
    monkeypatch.setattr(
        "fas_watch.find_run",
        lambda repository, sha, runner=None: WorkflowRun(1, "completed", "success", sha, "FAS CI"),
    )
    assert watch_and_recover("owner/repo", repair_runner=lambda task: 0, runner=lambda *a, **k: None) == "success"


def test_watch_recovers_one_actionable_failure(monkeypatch):
    monkeypatch.setattr("fas_watch.current_sha", lambda repository, runner=None: "abc")
    monkeypatch.setattr(
        "fas_watch.find_run",
        lambda repository, sha, runner=None: WorkflowRun(7, "completed", "failure", sha, "FAS CI"),
    )
    seen = []
    monkeypatch.setattr(
        "fas_watch.recover_once",
        lambda repository, run_id, repair_runner: seen.append((repository, run_id)) or 0,
    )
    assert watch_and_recover("owner/repo", repair_runner=lambda task: 0, runner=lambda *a, **k: None) == "repaired"
    assert seen == [("owner/repo", 7)]


def test_watch_stops_when_repair_fails(monkeypatch):
    monkeypatch.setattr("fas_watch.current_sha", lambda repository, runner=None: "abc")
    monkeypatch.setattr(
        "fas_watch.find_run",
        lambda repository, sha, runner=None: WorkflowRun(7, "completed", "failure", sha, "FAS CI"),
    )
    monkeypatch.setattr("fas_watch.recover_once", lambda *args, **kwargs: 1)
    assert watch_and_recover("owner/repo", repair_runner=lambda task: 1, runner=lambda *a, **k: None) == "repair_failed"


def test_watch_never_repairs_non_actionable_runs(monkeypatch):
    monkeypatch.setattr("fas_watch.current_sha", lambda repository, runner=None: "abc")
    monkeypatch.setattr(
        "fas_watch.find_run",
        lambda repository, sha, runner=None: WorkflowRun(7, "completed", "timed_out", sha, "FAS CI"),
    )
    called = []
    monkeypatch.setattr("fas_watch.recover_once", lambda *args, **kwargs: called.append(1) or 0)
    assert watch_and_recover("owner/repo", repair_runner=lambda task: 0, runner=lambda *a, **k: None) == "non_actionable"
    assert called == []


def test_watch_rejects_zero_budget():
    with pytest.raises(ValueError, match="positive"):
        watch_and_recover("owner/repo", max_attempts=0, repair_runner=lambda task: 0)
