from pathlib import Path
import subprocess

import fas_cli


def test_cli_init_delegates_to_portable_state(monkeypatch, tmp_path, capsys):
    expected = tmp_path / ".fas" / "state.json"
    monkeypatch.setattr(fas_cli, "init_repository", lambda repo: expected)
    assert fas_cli.main(["init", str(tmp_path)]) == 0
    assert str(expected) in capsys.readouterr().out


def test_cli_run_uses_router_model_when_no_override(monkeypatch, tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    calls = []
    state = {
        "schema_version": 1,
        "repository": str(repo.resolve()),
        "phase": "READ",
        "attempt": 0,
        "max_attempts": 3,
        "route": None,
        "test": {},
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
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(fas_cli.subprocess, "run", fake_run)
    monkeypatch.setattr(fas_cli, "record_test", lambda *args: Path(tmp_path / "recorded.json"))

    assert fas_cli.main(["run", "do work", "--repo", str(repo)]) == 0
    command = calls[0][0]
    assert command[:7] == [
        "opencode", "run", "--auto", "--model", "custom/model", "--agent", "build"
    ]
    assert command[-1] == "do work"


def test_cli_model_override_is_effective_but_router_choice_remains_planned(monkeypatch, tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    base = {
        "schema_version": 1,
        "repository": str(repo.resolve()),
        "phase": "READ",
        "attempt": 0,
        "max_attempts": 3,
        "route": None,
        "test": {},
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
    monkeypatch.setattr(fas_cli.subprocess, "run", lambda command, **kwargs: subprocess.CompletedProcess(command, 0))
    monkeypatch.setattr(fas_cli, "record_test", lambda *args: None)
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
