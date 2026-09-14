import fas_cli


def _state(result="success", failure=None):
    return {
        "attempt": 0,
        "ci": {"run_id": 9, "result": result},
        "failure": failure or {"class": None, "stage": None, "message": None},
        "test": {"command": None, "result": None, "duration_seconds": None},
        "git": {"branch": "main", "commit_sha": None},
    }


def test_cli_watch_delegates_to_bounded_watch_and_prints_report(monkeypatch, tmp_path, capsys):
    captured = {}

    def fake_watch(repo, **kwargs):
        captured["repo"] = repo
        captured.update(kwargs)
        return "success"

    monkeypatch.setattr(fas_cli, "watch_and_recover", fake_watch)
    monkeypatch.setattr(fas_cli, "init_repository", lambda repo: None)
    monkeypatch.setattr(fas_cli, "current_sha", lambda repo: "abc")
    monkeypatch.setattr(fas_cli, "read_state", lambda repo: _state())
    monkeypatch.setattr(fas_cli, "write_report", lambda repo, report: repo)
    assert fas_cli.main(["watch", "--repo", str(tmp_path), "--max-attempts", "2", "--poll-limit", "4", "--poll-seconds", "0.1", "--test-cmd", "pytest -q"]) == 0
    assert captured["repo"] == str(tmp_path.resolve())
    assert captured["max_attempts"] == 2
    assert captured["poll_limit"] == 4
    assert captured["poll_seconds"] == 0.1
    output = capsys.readouterr().out
    assert "=== FAS AUTONOMOUS RECOVERY REPORT ===" in output
    assert "STATUS: PASS" in output
    assert "RESULT: success" in output


def test_cli_watch_returns_nonzero_for_terminal_failure_with_report(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(fas_cli, "watch_and_recover", lambda repo, **kwargs: "scope_violation")
    monkeypatch.setattr(fas_cli, "init_repository", lambda repo: None)
    monkeypatch.setattr(fas_cli, "current_sha", lambda repo: "abc")
    monkeypatch.setattr(fas_cli, "read_state", lambda repo: _state("failure", {"class": "scope_violation", "stage": "RECOVERY / SCOPE VALIDATION", "message": "Repair changed a path outside the declared recovery scope."}))
    monkeypatch.setattr(fas_cli, "write_report", lambda repo, report: repo)
    assert fas_cli.main(["watch", "--repo", str(tmp_path)]) == 1
    output = capsys.readouterr().out
    assert "STATUS: FAIL" in output
    assert "CLASS: scope_violation" in output
    assert "RECOVERY / SCOPE VALIDATION" in output
    assert "RECOMMENDATION:" in output
