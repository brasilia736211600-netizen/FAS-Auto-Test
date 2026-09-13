import fas_autopilot


def test_autopilot_stops_after_requested_successful_cycle(monkeypatch, tmp_path):
    calls = []
    monkeypatch.setattr(fas_autopilot, "_watch", lambda args: calls.append(args.repo) or 0)
    assert fas_autopilot.run(
        tmp_path,
        max_attempts=2,
        poll_limit=3,
        poll_seconds=0.1,
        idle_seconds=0.1,
        max_cycles=1,
    ) == 0
    assert calls == [str(tmp_path.resolve())]
