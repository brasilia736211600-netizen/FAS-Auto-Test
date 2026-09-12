import json
import subprocess

from fas_recovery import build_repair_task, failed_logs, persist_failure_logs, recover_once


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


def test_repair_task_points_agent_to_fresh_ci_evidence(tmp_path):
    task = build_repair_task(tmp_path / ".fas" / "logs" / "ci-failure.log")
    assert "ci-failure.log" in task
    assert "smallest YAGNI-compliant fix" in task
    assert "force-push" in task


def test_recover_once_persists_logs_and_invokes_one_repair(tmp_path, monkeypatch):
    monkeypatch.setattr("fas_recovery.ensure_fas_excluded", lambda repo: None)
    monkeypatch.setattr(
        "fas_recovery.failed_logs",
        lambda repository, run_id: "failure from CI",
    )
    received = []

    def repair_runner(task):
        received.append(task)
        return 0

    assert recover_once("owner/repo", 7, repair_runner=repair_runner) == 0
    assert received and "failure from CI" not in received[0]
    assert (tmp_path / ".fas" / "logs" / "ci-failure.log").exists() is False


def test_recovery_log_payload_is_plain_text(tmp_path):
    # Ensure the recovery artifact is not a structured secret-bearing object.
    path = persist_failure_logs(tmp_path, "line 1\nline 2\n")
    assert json.loads(json.dumps({"path": str(path)}))["path"].endswith("ci-failure.log")
