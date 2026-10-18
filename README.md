# codex-config

現在のCodex設定を別のPCへ移すためのリポジトリです。ユーザー名や作業フォルダに依存する設定は含めず、通知スクリプトは `CODEX_HOME`（未設定なら `~/.codex`）から読み込みます。

| ファイル | 内容 |
| --- | --- |
| `config.toml` | モデル・推論設定、プラグイン、マーケットプレイス、Codegraph MCP |
| `AGENTS.md` | グローバル指示（現在は空） |
| `skills/` | 現在のローカルスキル一式 |
| `rules/default.rules` | 端末やセッションに依存しない実行許可ルール |
| `notify.py` | ntfyへの完了通知。サブエージェントの通知は抑制 |

## 別のPCへの取り込み

CodexとPython 3をインストールし、Codexにログインしてください。以下はmacOS・Linux・WSLのシェル用です。リポジトリは任意の場所にcloneし、そのディレクトリで実行します。既存ファイルを置き換える場合は先にバックアップしてください。`-i` により、同名ファイルを上書きするときに確認します。

```sh
codex_config_home="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$codex_config_home/skills" "$codex_config_home/rules"
cp -i config.toml notify.py AGENTS.md "$codex_config_home/"
cp -Ri skills/. "$codex_config_home/skills/"
cp -Ri rules/. "$codex_config_home/rules/"
```

Windowsを直接使う場合は、同じファイルを `%USERPROFILE%\.codex` または `CODEX_HOME` で指定したフォルダへコピーし、`python3` コマンドが使えるようにしてください。

Codegraph MCPを使う場合は、移行先でも `codegraph` コマンドをPATHから実行できるようにしてください。現在の環境では `@colbymchenry/codegraph` 1.6.0を使っています。

プラグイン本体はリポジトリに含めていません。Codexのプラグイン画面で `config.toml` に記載したプラグインをインストールし、連携サービスを認証してください。外部マーケットプレイスのURLとSuperpowersの固定リビジョンは設定に含めています。CLIで操作する場合は `codex plugin marketplace list` と `codex plugin list` で確認できます。[公式プラグインドキュメント](https://developers.openai.com/plugins/build/plugins)も参照してください。

信頼するプロジェクトは、移行先の実際の絶対パスで個別に設定してください。例は `config.toml` 内のコメントにあります。フックの信頼確認も移行先で行ってください。

## ntfy通知

通知を使う場合は、他人と共有しない通知先トピックを環境変数に設定してからCodexを起動してください。

```sh
export NTFY_TOPIC="your-private-codex-topic"
```

`NTFY_TOPIC` が未設定または空の場合、通知は送信しません。設定すると、メインエージェントの最終応答を `https://ntfy.sh/<トピック名>` へ送信します。デスクトップアプリで使う場合も、起動するアプリにこの環境変数を渡してください。

## 移行対象から除外するもの

認証情報、会話履歴、添付ファイル、キャッシュ、データベース、個別プロジェクトの信頼設定、セッション固有の実行許可、UIの確認済み状態、フックの承認記録は保存しません。これらの設定は必要に応じて移行先で作成します。

Codexのユーザー設定は `~/.codex/config.toml` に置きます。設定項目の詳細は[公式設定リファレンス](https://learn.chatgpt.com/docs/config-file/config-reference)を参照してください。

## 動作確認

Python 3.11以上で実行します。通知先とサブエージェントの判定、空白を含むパスでの読み込みを確認し、外部への通知は送信しません。

```sh
python3 -m unittest -v test_notify
```
