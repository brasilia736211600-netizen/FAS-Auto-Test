import os
import subprocess

from fas_recovery import (
    build_repair_task,
    failed_logs,
    persist_failure_logs,
    recover_once,
    recovery_scope,
    workflow_file,
)


def test_failed_logs_uses_gh_run_view_log_failed():
    calls = []

    def runner(command, **kwargs):
        calls.append(command)
        return subprocess.CompletedProcess(command, 0, "FAIL LOG\n", "")

    assert failed_logs("owner/repo", 42, runner=runner) == "FAIL LOG\n"
    assert calls == [["gh", "run", "view", "42", "--repo", "owner/repo", "--log-failed"]]


def test_persist_failure_logs_writes_under_local_fas_state(tmp_path, monkeypatch):
    monkeypatch.setattr("fas_recovery.ensure_fas_excluded", lambda repo: None)
    path = persist_failure_logs(tmp_path, "failure evidence")
    assert path == tmp_path / ".fas" / "logs" / "ci-failure.log"
    assert path.read_text(encoding="utf-8") == "failure evidence"


def test_recovery_scope_resolves_unique_failed_test_path(tmp_path):
    e2e = tmp_path / "e2e"
    e2e.mkdir()
    (e2e / "test_live_fixture.py").write_text("assert True\n", encoding="utf-8")
    logs = "FAILED test_live_fixture.py::test_addition - assert -1 == 5"
    assert recovery_scope(tmp_path, logs) == ("e2e/",)


def test_recovery_scope_finds_paths_printed_by_ci_commands(tmp_path):
    workflow = tmp_path / ".github" / "workflows"
    workflow.mkdir(parents=True)
    target = tmp_path / "apps" / "weblibre" / "profile.g.dart"
    target.parent.mkdir(parents=True)
    target.write_text("generated\n", encoding="utf-8")
    logs = "Expected exactly one profile.g.dart, found 1:\napps/weblibre/profile.g.dart"
    assert recovery_scope(tmp_path, logs) == ("apps/weblibre/",)


def test_recovery_scope_rejects_ambiguous_path(tmp_path):
    (tmp_path / "one").mkdir()
    (tmp_path / "two").mkdir()
    for directory in (tmp_path / "one", tmp_path / "two"):
        (directory / "test_same.py").write_text("assert True\n", encoding="utf-8")
    logs = "FAILED test_same.py::test_case"
    assert recovery_scope(tmp_path, logs) == ()


def test_workflow_file_resolves_failed_workflow_name(tmp_path):
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "ci.yml").write_text("name: Profile Codegen TDD\n", encoding="utf-8")

    def runner(command, **kwargs):
        if command[:3] == ["git", "-C", str(tmp_path.resolve())]:
            return subprocess.CompletedProcess(command, 0, "https://github.com/owner/repo.git\n", "")
        return subprocess.CompletedProcess(command, 0, '{"workflowName":"Profile Codegen TDD"}\n', "")

    assert workflow_file(tmp_path, 42, runner=runner) == ".github/workflows/ci.yml"


def test_repair_task_points_agent_to_fresh_ci_evidence(tmp_path):
    task = build_repair_task(
        tmp_path / ".fas" / "logs" / "ci-failure.log",
        ("e2e/",),
    )
    assert "ci-failure.log" in task
    assert "smallest YAGNI-compliant fix" in task
    assert "force-push" in task
    assert "e2e/" in task


def test_recover_once_persists_logs_and_passes_scope_to_repair(tmp_path, monkeypatch):
    monkeypatch.setattr("fas_recovery.ensure_fas_excluded", lambda repo: None)
    monkeypatch.setattr(
        "fas_recovery.failed_logs",
        lambda repository, run_id: "FAILED test_live_fixture.py::test_addition",
    )
    monkeypatch.setattr("fas_recovery.workflow_file", lambda repository, run_id: None)
    e2e = tmp_path / "e2e"
    e2e.mkdir()
    (e2e / "test_live_fixture.py").write_text("assert True\n", encoding="utf-8")
    received = []

    def repair_runner(task):
        received.append(task)
        return 0

    assert recover_once(str(tmp_path), 7, repair_runner=repair_runner) == 0
    assert received and "e2e/" in received[0]
    assert (tmp_path / ".fas" / "logs" / "ci-failure.log").read_text(encoding="utf-8").startswith("FAILED")
    assert monkeypatch is not None


def test_recover_once_sets_dedicated_commit_message_and_restores_environment(tmp_path, monkeypatch):
    monkeypatch.setattr("fas_recovery.ensure_fas_excluded", lambda repo: None)
    monkeypatch.setattr(
        "fas_recovery.failed_logs",
        lambda repository, run_id: "FAILED test_live_fixture.py::test_addition",
    )
    monkeypatch.setattr("fas_recovery.workflow_file", lambda repository, run_id: None)
    e2e = tmp_path / "e2e"
    e2e.mkdir()
    (e2e / "test_live_fixture.py").write_text("assert True\n", encoding="utf-8")
    monkeypatch.setenv("FAS_COMMIT_MESSAGE", "stale message")
    seen = []

    def repair_runner(task):
        seen.append(os.environ.get("FAS_COMMIT_MESSAGE"))
        return 0

    assert recover_once(str(tmp_path), 7, repair_runner=repair_runner) == 0
    assert seen == ["fix: autonomous CI recovery"]
    assert os.environ["FAS_COMMIT_MESSAGE"] == "stale message"


def test_recover_once_stops_when_scope_is_unknown(tmp_path, monkeypatch):
    monkeypatch.setattr("fas_recovery.ensure_fas_excluded", lambda repo: None)
    monkeypatch.setattr("fas_recovery.failed_logs", lambda repository, run_id: "no concrete path")
    monkeypatch.setattr("fas_recovery.workflow_file", lambda repository, run_id: None)
    called = []
    assert recover_once(str(tmp_path), 7, repair_runner=lambda task: called.append(task) or 0) == 77
    assert called == []
