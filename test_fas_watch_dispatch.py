from __future__ import annotations

import json
import subprocess
import unittest

from fas_watch import watch_and_recover


class MissingRunDispatchTests(unittest.TestCase):
    def test_missing_run_handler_fires_once_before_success(self) -> None:
        sha = "a" * 40
        calls = []
        run_payload = [
            {
                "databaseId": 42,
                "status": "completed",
                "conclusion": "success",
                "headSha": sha,
                "workflowName": "validation",
            }
        ]
        gh_calls = 0

        def runner(command, **kwargs):
            nonlocal gh_calls
            if command[:4] == ["git", "-C", "/repo", "rev-parse"]:
                return subprocess.CompletedProcess(command, 0, stdout=sha + "\n", stderr="")
            if command[:3] == ["gh", "run", "list"]:
                gh_calls += 1
                payload = [] if gh_calls == 1 else run_payload
                return subprocess.CompletedProcess(command, 0, stdout=json.dumps(payload), stderr="")
            raise AssertionError(command)

        result = watch_and_recover(
            "/repo",
            max_attempts=1,
            poll_limit=3,
            poll_seconds=0,
            runner=runner,
            repair_runner=lambda _task: 0,
            missing_run_handler=calls.append,
        )

        self.assertEqual(result, "success")
        self.assertEqual(calls, [sha])


if __name__ == "__main__":
    unittest.main()
