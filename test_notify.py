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
                    self.assertEqual(request.full_url, "https://ntfy.sh/test-topic")
                    self.assertEqual(request.data, "完了".encode())

    def test_subagent_sessions_use_codex_home(self):
        with tempfile.TemporaryDirectory(prefix="codex home ") as temporary:
            session = Path(temporary) / "sessions/2026/01/01/rollout-test-thread.jsonl"
            session.parent.mkdir(parents=True)
            session.write_text(json.dumps({
                "type": "session_meta", "payload": {"parent_thread_id": "parent"},
            }) + "\n", encoding="utf-8")
            with patch.dict(os.environ, {"CODEX_HOME": temporary}):
                self.assertTrue(notify.is_subagent("test-thread"))

    def test_config_launcher_resolves_home_and_preserves_event(self):
        config = tomllib.loads(Path(__file__).with_name("config.toml").read_text())
        self.assertFalse(any(str(Path.home()) in arg for arg in config["notify"]))
        event = '{"type":"agent-turn-complete"}'
        with tempfile.TemporaryDirectory(prefix="codex home ") as temporary:
            for custom in (False, True):
                with self.subTest(custom_codex_home=custom):
                    root = Path(temporary) / ("custom home" if custom else ".codex")
                    root.mkdir()
                    (root / "notify.py").write_text("import sys; print(sys.argv[1])\n")
                    env = dict(os.environ, HOME=temporary, USERPROFILE=temporary)
                    env.pop("CODEX_HOME", None)
                    if custom:
                        env["CODEX_HOME"] = str(root)
                    result = subprocess.run(config["notify"] + [event], env=env,
                                            cwd=temporary, check=True,
                                            capture_output=True, text=True)
                    self.assertEqual(result.stdout.strip(), event)


if __name__ == "__main__":
    unittest.main()
