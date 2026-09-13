from pathlib import Path
import subprocess
from types import SimpleNamespace

import fas_cli


def test_cli_init_delegates_to_portable_state(monkeypatch, tmp_path, capsys):
    expected = tmp_path / ".fas" / "state.json"
    monkeypatch.setattr(fas_cli, "init_repository", lambda repo: expected)
    assert fas_cli.main(["init", str(tmp_path)]) == 0
    assert str(expected) in capsys.readouterr().out


def test_cli_run_bootstraps_state_and_uses_router_model(monkeypatch, tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".fas").mkdir()
    (repo / ".fas" / "state.json").write_text("{}", encoding="utf-8")
    calls = []
    state = {
        "schema_version": 1,
        "repository": str(repo.resolve()),
        "phase": "READ",
        "attempt": 0,
        "max_attempts": 3,
        "route": None,
        "test": {},
        "git": {"branch": None, "commit_sha": None},
    }

    monkeypatch.setattr(fas_cli, "read_state", lambda _: state.copy())
    monkeypatch.setattr(
        fas_cli,
        "select_route",
        lambda *_: {"capability": "fast_simple", "model": "custom/model", "reason": "test"},
    )
    monkeypatch.setattr(fas_cli, "status_porcelain", lambda _: "")
    monkeypatch.setattr(fas_cli, "changed_after", lambda *_: False)
    monkeypatch.setattr(fas_cli, "write_state", lambda *_args, **_kwargs: Path(tmp_path / "state.json"))

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        stdout = ""
        if "branch" in command and "--show-current" in command:
            stdout = "main\n"
        if command and command[-1] == "HEAD":
            stdout = "abc123\n"
        return subprocess.CompletedProcess(command, 0, stdout=stdout)

    monkeypatch.setattr(fas_cli.subprocess, "run", fake_run)
    monkeypatch.setattr(fas_cli, "record_test", lambda *args: Path(tmp_path / "recorded.json"))
    monkeypatch.delenv("FAS_PUSH", raising=False)
    monkeypatch.delenv("FAS_COMMIT", raising=False)

    assert fas_cli.main(["run", "do work", "--repo", str(repo)]) == 0
    command = calls[0][0]
    assert command[:7] == [
        "opencode", "run", "--auto", "--model", "custom/model", "--agent", "build"
    ]
    assert command[-1] == "do work"


def test_cli_model_override_is_effective_but_router_choice_remains_planned(monkeypatch, tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".fas").mkdir()
    (repo / ".fas" / "state.json").write_text("{}", encoding="utf-8")
    base = {
        "schema_version": 1,
        "repository": str(repo.resolve()),
        "phase": "READ",
        "attempt": 0,
        "max_attempts": 3,
        "route": None,
        "test": {},
        "git": {"branch": None, "commit_sha": None},
    }
    persisted = []

    monkeypatch.setattr(fas_cli, "read_state", lambda _: base.copy())
    monkeypatch.setattr(
        fas_cli,
        "select_route",
        lambda *_: {"capability": "fast_simple", "model": "planned/model", "reason": "test"},
    )
    monkeypatch.setattr(fas_cli, "status_porcelain", lambda _: "")
    monkeypatch.setattr(fas_cli, "changed_after", lambda *_: False)
    monkeypatch.setattr(
        fas_cli,
        "write_state",
        lambda _repo, value: persisted.append(value) or Path(tmp_path / "state.json"),
    )
    def fake_run(command, **kwargs):
        stdout = ""
        if "branch" in command and "--show-current" in command:
            stdout = "main\n"
        if command and command[-1] == "HEAD":
            stdout = "abc123\n"
        return subprocess.CompletedProcess(command, 0, stdout=stdout)

    monkeypatch.setattr(fas_cli.subprocess, "run", fake_run)
    monkeypatch.setattr(fas_cli, "record_test", lambda *args: None)
    monkeypatch.delenv("FAS_PUSH", raising=False)
    monkeypatch.delenv("FAS_COMMIT", raising=False)
    monkeypatch.setenv("FAS_MODEL", "override/model")

    assert fas_cli.main(["run", "do work", "--repo", str(repo)]) == 0
    assert persisted[-1]["route"]["model"] == "planned/model"
    assert persisted[-1]["route"]["effective_model"] == "override/model"


def test_cli_parser_requires_task_for_run():
    try:
        fas_cli.main(["run"])
    except SystemExit as exc:
        assert exc.code != 0
    else:
        raise AssertionError("run without task must be rejected")


def _cli_success_state(monkeypatch, tmp_path, *, persisted=None):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".fas").mkdir()
    (repo / ".fas" / "state.json").write_text("{}", encoding="utf-8")
    base = {
        "schema_version": 1,
        "repository": str(repo.resolve()),
        "phase": "READ",
        "attempt": 0,
        "max_attempts": 3,
        "route": None,
        "test": {},
        "git": {"branch": None, "commit_sha": None},
    }
    monkeypatch.setattr(fas_cli, "read_state", lambda _: base.copy())
    monkeypatch.setattr(
        fas_cli,
        "select_route",
        lambda *_: {"capability": "fast_simple", "model": "planned/model", "reason": "test"},
    )
    monkeypatch.setattr(fas_cli, "status_porcelain", lambda _: "")
    monkeypatch.setattr(fas_cli, "changed_after", lambda *_: False)
    monkeypatch.setattr(fas_cli, "run_with_fallback", lambda *args, **kwargs: SimpleNamespace(success=True, attempts=[], selected_model="planned/model"))
    monkeypatch.setattr(fas_cli, "record_test", lambda *args: None)
    if persisted is None:
        monkeypatch.setattr(fas_cli, "write_state", lambda *_args, **_kwargs: Path(tmp_path / "state.json"))
    else:
        monkeypatch.setattr(
            fas_cli,
            "write_state",
            lambda _repo, value: persisted.append(value) or Path(tmp_path / "state.json"),
        )
    return repo


def test_cli_test_failure_blocks_commit_and_push(monkeypatch, tmp_path):
    repo = _cli_success_state(monkeypatch, tmp_path)
    monkeypatch.setenv("FAS_COMMIT", "1")
    monkeypatch.setenv("FAS_PUSH", "1")
    monkeypatch.setattr(
        fas_cli.subprocess,
        "run",
        lambda command, **kwargs: subprocess.CompletedProcess(command, 1, stdout="", stderr="test failed"),
    )
    monkeypatch.setattr(fas_cli, "commit_if_changed", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("commit must not run")))
    monkeypatch.setattr(fas_cli, "safe_push", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("push must not run")))

    assert fas_cli.main(["run", "do work", "--repo", str(repo), "--test-cmd", "pytest -q"]) == 1


def test_cli_recovery_requires_explicit_scope_before_commit(monkeypatch, tmp_path):
    persisted = []
    repo = _cli_success_state(monkeypatch, tmp_path, persisted=persisted)
    monkeypatch.setenv("FAS_COMMIT", "1")
    monkeypatch.setenv("FAS_PUSH", "1")
    monkeypatch.delenv("FAS_ALLOWED_PATHS", raising=False)
    monkeypatch.setattr(
        fas_cli.subprocess,
        "run",
        lambda command, **kwargs: subprocess.CompletedProcess(command, 0, stdout="", stderr=""),
    )
    monkeypatch.setattr(fas_cli, "commit_if_changed", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("commit must not run")))
    monkeypatch.setattr(fas_cli, "safe_push", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("push must not run")))

    assert fas_cli.main(["run", "do work", "--repo", str(repo), "--recovery", "--test-cmd", "pytest -q"]) == 77
    assert persisted[-1]["failure"]["class"] == "scope_unknown"
