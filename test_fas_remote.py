from __future__ import annotations

import os
import subprocess
import unittest

import fas_remote
from fas_remote import RemoteTarget, remote_head, run_remote, wait_for_remote_change


class RemoteHelpersTests(unittest.TestCase):
    def test_remote_head_reads_ls_remote_sha(self) -> None:
        sha = "0123456789abcdef0123456789abcdef01234567"

        def runner(command, **kwargs):
            self.assertEqual(command[-1], "refs/heads/main")
            return subprocess.CompletedProcess(command, 0, stdout=f"{sha}\trefs/heads/main\n", stderr="")

        self.assertEqual(remote_head("owner/repo", "main", runner=runner), sha)

    def test_wait_for_remote_change_returns_new_sha(self) -> None:
        target = RemoteTarget("owner/repo", "main")
        old = "0" * 40
        new = "1" * 40
        values = iter([old, new])

        def runner(command, **kwargs):
            sha = next(values)
            return subprocess.CompletedProcess(command, 0, stdout=f"{sha}\trefs/heads/main\n", stderr="")

        self.assertEqual(
            wait_for_remote_change(target, old, poll_seconds=0, runner=runner, poll_limit=2),
            new,
        )

    def test_remote_autopilot_uses_disposable_checkout_and_watch(self) -> None:
        target = RemoteTarget("owner/repo", "main")
        sha = "2" * 40
        commands = []

        def runner(command, **kwargs):
            commands.append(command)
            if command[:2] == ["git", "ls-remote"]:
                return subprocess.CompletedProcess(command, 0, stdout=f"{sha}\trefs/heads/main\n", stderr="")
            if command[:2] == ["git", "clone"]:
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

        def watch(args):
            self.assertTrue(args.repo.startswith("/"))
            self.assertEqual(args.max_attempts, 1)
            return 0

        result = run_remote(
            target,
            max_attempts=1,
            poll_limit=1,
            poll_seconds=0,
            idle_seconds=0,
            max_cycles=1,
            runner=runner,
            watch_runner=watch,
        )
        self.assertEqual(result, "success")
        self.assertTrue(any(command[:2] == ["git", "clone"] for command in commands))

    def test_remote_retries_after_failed_watch_with_fresh_checkout_and_context(self) -> None:
        target = RemoteTarget("owner/repo", "main")
        sha = "3" * 40
        contexts = []
        calls = 0

        def runner(command, **kwargs):
            if command[:2] == ["git", "ls-remote"]:
                return subprocess.CompletedProcess(command, 0, stdout=f"{sha}\trefs/heads/main\n", stderr="")
            if command[:2] == ["git", "clone"]:
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

        def watch(args):
            nonlocal calls
            calls += 1
            contexts.append(os.environ.get("FAS_RETRY_CONTEXT"))
            return 1 if calls == 1 else 0

        result = run_remote(
            target,
            max_attempts=2,
            poll_limit=1,
            poll_seconds=0,
            idle_seconds=0,
            max_cycles=1,
            runner=runner,
            watch_runner=watch,
        )
        self.assertEqual(result, "success")
        self.assertEqual(calls, 2)
        self.assertIsNone(contexts[0])
        self.assertIn("different minimal repair", contexts[1])

    def test_mission_mode_requires_explicit_scope(self) -> None:
        with self.assertRaises(ValueError):
            run_remote(RemoteTarget("owner/repo", "main"), objective="do the task", max_cycles=1)

    def test_mission_mode_runs_before_ci_watch(self) -> None:
        target = RemoteTarget("owner/repo", "main")
        events = []
        sha = "4" * 40

        def runner(command, **kwargs):
            if command[:2] == ["git", "ls-remote"]:
                return subprocess.CompletedProcess(command, 0, stdout=f"{sha}\trefs/heads/main\n", stderr="")
            if command[:2] == ["git", "clone"]:
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

        original = fas_remote._run_clean_task
        try:
            fas_remote._run_clean_task = lambda *args, **kwargs: events.append(("mission", args[1], kwargs["scope_paths"])) or 0

            def watch(args):
                events.append(("watch", args.repo))
                return 0

            result = run_remote(
                target,
                objective="complete CP3 then CP4 and CP5",
                scope_paths=("modules/nora-view/android/", "security/", ".github/workflows/", "docs/", "app.config.ts"),
                max_attempts=1,
                poll_limit=1,
                poll_seconds=0,
                idle_seconds=0,
                max_cycles=1,
                runner=runner,
                watch_runner=watch,
            )
        finally:
            fas_remote._run_clean_task = original

        self.assertEqual(result, "success")
        self.assertEqual(events[0][0], "mission")
        self.assertIn("CP3", events[0][1])
        self.assertEqual(events[1][0], "watch")


if __name__ == "__main__":
    unittest.main()
