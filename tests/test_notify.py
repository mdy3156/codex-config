import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import notify


class NotifyTests(unittest.TestCase):
    def test_task_title_and_japanese_json(self):
        event = {"type": "agent-turn-complete", "cwd": "/work/codex-config",
                 "input-messages": ["古い依頼", "通知タイトルを改善して\n詳細です"],
                 "last-assistant-message": "改善しました。"}
        with patch.object(sys, "argv", ["notify.py", "--dry-run", json.dumps(event)]):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(notify.main(), 0)
        payload = json.loads(output.getvalue())
        self.assertIn("codex-config", payload["title"])
        self.assertIn("通知タイトルを改善して", payload["title"])
        self.assertNotIn("詳細です", payload["title"])
        self.assertEqual(payload["message"], "改善しました。")

    def test_subagent_with_custom_codex_home_is_suppressed(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / "codex[personal]"
            path = home / "sessions/2026/10/19/rollout-test-abc.jsonl"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({"type": "session_meta", "payload": {
                "source": {"subagent": {"thread_spawn": {"parent_thread_id": "parent"}}}
            }}) + "\n")
            result = subprocess.run([sys.executable, "notify.py", "--dry-run",
                                     "--codex-home", str(home), json.dumps({
                                         "type": "agent-turn-complete", "thread-id": "abc"})],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")

    def test_invalid_payload_reports_error_without_traceback(self):
        for value in ("{", "[]", '{"type":"agent-turn-complete","cwd":42}'):
            result = subprocess.run([sys.executable, "notify.py", value],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Traceback", result.stderr)

    def test_fallback_title_and_length(self):
        for event in ({"last-assistant-message": "実装しました"},
                      {"input-messages": ["あ" * 200]}, {}):
            payload = notify.notification_payload(event)
            self.assertTrue(payload["title"].strip())
            self.assertLessEqual(len(payload["title"]), 100)

    def test_publish_uses_ntfy_json_endpoint_and_reports_timeout(self):
        event = json.dumps({"type": "agent-turn-complete", "input-messages": ["日本語の依頼"]})
        requests = []

        def receive(request, timeout):
            requests.append(request)
            return MagicMock()

        with patch.object(sys, "argv", ["notify.py", event]), patch.dict(os.environ, {"NTFY_TOPIC": "test-topic"}):
            with patch.object(notify.urllib.request, "urlopen", side_effect=receive):
                self.assertEqual(notify.main(), 0)
            with patch.object(notify.urllib.request, "urlopen", side_effect=TimeoutError("timed out")):
                output = io.StringIO()
                with contextlib.redirect_stderr(output):
                    self.assertEqual(notify.main(), 1)
                self.assertNotIn("Traceback", output.getvalue())
        self.assertEqual(requests[0].full_url, "https://ntfy.sh/")
        self.assertEqual(requests[0].get_header("Content-type"), "application/json")
        self.assertIn("日本語の依頼", json.loads(requests[0].data)["title"])


if __name__ == "__main__":
    unittest.main()
