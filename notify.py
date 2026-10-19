#!/usr/bin/env python3
"""Send Codex turn completion to ntfy, with a project and task in the title."""
import argparse
import glob
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.request


def is_subagent(thread_id: str, codex_home=None) -> bool:
    home = Path(codex_home or os.environ.get("CODEX_HOME", "~/.codex")).expanduser()
    pattern = glob.escape(str(home)) + "/sessions/*/*/*/rollout-*" + glob.escape(thread_id) + "*.jsonl"
    # notify と rollout 書き込みが僅かに前後する可能性への対策。
    for _ in range(5):
        paths = glob.glob(pattern)
        if paths:
            try:
                path = max(paths, key=os.path.getmtime)
                with open(path, encoding="utf-8") as handle:
                    first = json.loads(handle.readline())
                if first.get("type") != "session_meta":
                    return False
                meta = first.get("payload", {})
                source = meta.get("source")
                return bool(meta.get("parent_thread_id") or
                            isinstance(source, dict) and "subagent" in source)
            except (OSError, ValueError, AttributeError, TypeError):
                return False
        time.sleep(0.1)
    # 判別不能ならメイン通知を取りこぼさない。
    return False


def notification_payload(data):
    if not isinstance(data, dict):
        raise ValueError("Notification must be a JSON object")
    for key in ("cwd", "thread-id", "last-assistant-message"):
        if data.get(key) is not None and not isinstance(data[key], str):
            raise ValueError(f"{key} must be a string")
    messages = data.get("input-messages") or []
    if not isinstance(messages, list) or any(not isinstance(item, str) for item in messages):
        raise ValueError("input-messages must be a list of strings")
    task = next((item.strip() for item in reversed(messages) if item.strip()), "")
    task = task or data.get("last-assistant-message") or "ターン完了"
    task = next((line.strip() for line in task.splitlines() if line.strip()), "ターン完了")
    task = re.sub(r"^[#>*\-\s]+", "", task).strip("`* ") or "ターン完了"
    project = Path(data.get("cwd") or "").name or "Codex"
    title = f"{project[:30]}｜完了：{task}"
    if len(title) > 100:
        title = title[:99] + "…"
    return {"topic": os.environ.get("NTFY_TOPIC", os.environ.get("CODEX_NTFY_TOPIC", "")), "title": title,
            "message": data.get("last-assistant-message") or "Codexのターンが完了しました。",
            "priority": 3}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("event", nargs="?", help="Codex notification JSON")
    parser.add_argument("--codex-home", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="Print JSON without sending it")
    args = parser.parse_args()
    if args.event is None:
        return 0
    try:
        data = json.loads(args.event)
        if not isinstance(data, dict):
            raise ValueError("Notification must be a JSON object")
        if data.get("type") != "agent-turn-complete":
            return 0
        payload = notification_payload(data)
        if data.get("thread-id") and is_subagent(data["thread-id"], args.codex_home):
            return 0
        if args.dry_run:
            print(json.dumps(payload, ensure_ascii=False))
            return 0
        if not payload["topic"]:
            return 0
        request = urllib.request.Request(
            "https://ntfy.sh/", data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            method="POST", headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(request, timeout=10) as response:
            response.read()
    except (ValueError, OSError, urllib.error.URLError) as error:
        print(f"Codex notification failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
