import json

from fas_report import build_report, render_report, write_report


def test_build_report_captures_failure_details_and_recommendation(tmp_path):
    state = {
        "attempt": 1,
        "ci": {"run_id": 7, "result": "failure"},
        "failure": {
            "class": "scope_violation",
            "stage": "RECOVERY / SCOPE VALIDATION",
            "message": "Repair changed a path outside the declared recovery scope.",
        },
        "test": {"command": "pytest", "result": "PASS", "duration_seconds": 1.2},
        "git": {"branch": "fas-e2e-live", "commit_sha": None},
    }
    log_dir = tmp_path / ".fas" / "logs"
    log_dir.mkdir(parents=True)
    (log_dir / "ci-failure.log").write_text("failure", encoding="utf-8")

    report = build_report(
        repository=str(tmp_path),
        branch="fas-e2e-live",
        initial_sha="abc",
        final_sha="abc",
        result="scope_violation",
        state=state,
    )

    assert report["status"] == "FAIL"
    assert report["ci"]["run_id"] == 7
    assert report["failure"]["class"] == "scope_violation"
    assert report["recommendation"]
    assert report["ci_log"] == ".fas/logs/ci-failure.log"


def test_write_report_is_json_and_rendered_for_success(tmp_path):
    state = {
        "attempt": 0,
        "ci": {"run_id": 9, "result": "success"},
        "failure": {"class": None, "stage": None, "message": None},
        "test": {"command": None, "result": None, "duration_seconds": None},
        "git": {"branch": "fas-e2e-live", "commit_sha": "def"},
    }
    report = build_report(
        repository=str(tmp_path),
        branch="fas-e2e-live",
        initial_sha="abc",
        final_sha="def",
        result="success",
        state=state,
    )
    path = write_report(tmp_path, report)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    rendered = render_report(loaded)

    assert loaded["status"] == "PASS"
    assert "STATUS: PASS" in rendered
    assert "CI_RUN: 9" in rendered
    assert "COMMIT: def" in rendered
    assert loaded["test"]["result"] == "PASS"
    assert loaded["test"]["command"] == "GitHub Actions CI run 9"
    assert "TEST_RESULT: PASS" in rendered
