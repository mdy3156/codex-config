#!/usr/bin/env python3

import glob
import json
import os
import sys
import time
import urllib.request

TOPIC = "mdy-codex-9f"


def is_subagent(thread_id: str) -> bool:
    pattern = os.path.expanduser(
        f"~/.codex/sessions/*/*/*/rollout-*{thread_id}*.jsonl"
    )

    # notify と rollout 書き込みが僅かに前後する可能性への対策
    for _ in range(5):
        files = glob.glob(pattern)

        if files:
            path = max(files, key=os.path.getmtime)

            try:
                with open(path, "r", encoding="utf-8") as f:
                    first = json.loads(f.readline())

                if first.get("type") != "session_meta":
                    return False

                meta = first.get("payload", {})

                # 通常のサブエージェントなら親threadが存在する
                if meta.get("parent_thread_id"):
                    return True

                # 念のため source も確認
                source = meta.get("source")
                if isinstance(source, dict) and "subagent" in source:
                    return True

                return False

            except Exception:
                return False

        time.sleep(0.1)

    # 判別不能なら通知する（メイン通知を取りこぼさない）
    return False


def main():
    if len(sys.argv) < 2:
        return

    data = json.loads(sys.argv[1])

    if data.get("type") != "agent-turn-complete":
        return

    thread_id = data.get("thread-id")

    # ★ サブエージェントの完了通知は無視
    if thread_id and is_subagent(thread_id):
        return

    message = (
        data.get("last-assistant-message")
        or "Codex Done"
    )

    req = urllib.request.Request(
        f"https://ntfy.sh/{TOPIC}",
        data=message.encode("utf-8"),
        method="POST",
        headers={
            "Title": "Codex Done",
            "Priority": "default",
        },
    )

    urllib.request.urlopen(req, timeout=10).read()


if __name__ == "__main__":
    main()