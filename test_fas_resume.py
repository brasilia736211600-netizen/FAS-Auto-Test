from __future__ import annotations

from pathlib import Path

import fas_resume


def test_resume_routes_through_canonical_fas_runner(monkeypatch, tmp_path: Path):
    task_file = tmp_path / "task.md"
    task_file.write_text("task", encoding="utf-8")

    state = {
        "phase": "TEST",
        "attempt": 1,
        "max_attempts": 3,
        "git": {"commit_sha": "abc123"},
    }
    monkeypatch.setattr(fas_resume, "read_state", lambda _repo: state)

    calls: list[list[str]] = []

    def fake_fas_main(argv: list[str]) -> int:
        calls.append(argv)
        return 0

    monkeypatch.setattr(fas_resume, "fas_main", fake_fas_main)

    assert fas_resume.resume(tmp_path, str(task_file)) == 0
    assert calls
    argv = calls[0]
    assert argv[0] == "run"
    assert argv[1].startswith("RESUME an existing FAS-controlled task")
    assert "--repo" in argv
    assert str(tmp_path.resolve()) in argv
    assert "--architecture-impact" in argv
    assert "--files-changed" in argv


def test_build_resume_task_includes_durable_state(monkeypatch, tmp_path: Path):
    state = {
        "phase": "EXECUTE",
        "attempt": 2,
        "max_attempts": 3,
        "git": {"commit_sha": "deadbeef"},
    }
    monkeypatch.setattr(fas_resume, "read_state", lambda _repo: state)

    task = fas_resume.build_resume_task(tmp_path, "docs/task.md")
    assert "phase='EXECUTE'" in task
    assert "attempt=2" in task
    assert "commit_sha='deadbeef'" in task
    assert "canonical FAS runner" in task
