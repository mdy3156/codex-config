import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

import notify
import manage


class NotifyTests(unittest.TestCase):
    def test_topic_is_opt_in_and_subagents_are_skipped(self):
        event = json.dumps({
            "type": "agent-turn-complete",
            "thread-id": "test-thread",
            "last-assistant-message": "完了",
        })
        for topic, subagent, should_send in (
            (None, False, False), ("", False, False),
            ("test-topic", False, True), ("test-topic", True, False),
        ):
            with self.subTest(topic=topic, subagent=subagent), \
                    patch.dict(os.environ, {} if topic is None else
                               {"NTFY_TOPIC": topic}, clear=True), \
                    patch.object(sys, "argv", ["notify.py", event]), \
                    patch.object(notify, "is_subagent", return_value=subagent), \
                    patch.object(notify.urllib.request, "urlopen") as send:
                notify.main()
                self.assertEqual(send.called, should_send)
                if should_send:
                    request = send.call_args.args[0]
                    self.assertEqual(request.full_url, "https://ntfy.sh/")
                    self.assertEqual(json.loads(request.data)["topic"], "test-topic")
                    self.assertEqual(json.loads(request.data)["message"], "完了")

    def test_subagent_sessions_use_codex_home(self):
        with tempfile.TemporaryDirectory(prefix="codex home ") as temporary:
            session = Path(temporary) / "sessions/2026/01/01/rollout-test-thread.jsonl"
            session.parent.mkdir(parents=True)
            session.write_text(json.dumps({
                "type": "session_meta", "payload": {"parent_thread_id": "parent"},
            }) + "\n", encoding="utf-8")
            with patch.dict(os.environ, {"CODEX_HOME": temporary}):
                self.assertTrue(notify.is_subagent("test-thread"))

    def test_generated_launcher_preserves_event_in_path_with_spaces(self):
        event = '{"type":"agent-turn-complete"}'
        with tempfile.TemporaryDirectory(prefix="codex home ") as temporary:
            root = Path(temporary) / "custom home 日本語"
            with patch.object(manage, "fetch_skills", return_value={}), \
                    patch.object(manage.plugin_setup, "runtime_roots", return_value={}), \
                    patch.object(manage.plugin_setup, "install"):
                manage.install(root)
            config = tomllib.loads((root / "config.toml").read_text())
            # Replace the link so the fixture cannot overwrite the real notifier.
            (root / "notify.py").unlink()
            (root / "notify.py").write_text("import sys; print(sys.argv[-1])\n")
            result = subprocess.run(config["notify"] + [event], cwd=temporary, check=True,
                                    capture_output=True, text=True)
            self.assertEqual(result.stdout.strip(), event)


if __name__ == "__main__":
    unittest.main()
