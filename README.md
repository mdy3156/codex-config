# codex-config

Codexの共通設定、Skills、プラグイン、ntfy通知を管理する個人用リポジトリです。

## 導入

各環境にGit、Python 3.11以降、Node.js 22.20.0以降とnpm、`codex plugin` に対応したCodex CLIが必要です。Codexへのログインを先に済ませてください。

```sh
git clone https://github.com/mdy3156/codex-config.git
cd codex-config
./install.sh --dry-run
./install.sh
```

配置先は `$CODEX_HOME`、未設定なら `~/.codex` です。`--codex-home /path/to/codex` で変更できます。リポジトリは配置先とは別のディレクトリにcloneしてください。Pythonを指定する場合は `PYTHON=python3.14 ./install.sh` のように実行します。

Windowsアプリ向けにはWindows側のPowerShellで同じリポジトリから `python manage.py install` を実行します。更新は `python manage.py update` です。WSLはLinux側の `~/.codex`、Windowsアプリは `%USERPROFILE%\.codex` を使うため、それぞれの環境で実行してください。

共通プラグイン14個はCLIで自動導入します。アプリ付属11件の有効状態は `plugins.json` の `app_plugins` で別に管理し、その環境で提供されるものに適用します。付属設定を反映する環境では、先にアプリを一度起動してください。本体と実行環境の導入・更新はアプリが管理します。

## 更新

```sh
git pull --ff-only
./update.sh
```

導入と更新は同じ処理です。実行するたびに公開Skillsとプラグインの最新版を取得し、設定も適用します。アプリ付属プラグインは、そのアプリが提供する版を使います。Codexアプリ・CLI自体は別途更新してください。

`--dry-run` は通信・書き込みをせず、処理の予定を表示します。

## 管理するファイル

| ファイル | 用途 |
| --- | --- |
| [config.toml](config.toml) | 共通設定 |
| [AGENTS.md](AGENTS.md) | 資料作成に使うSkillsの選択 |
| [skills/requirements.json](skills/requirements.json) | 公開Skillsの名前と取得元 |
| [skills/custom/](skills/custom/) | 自作Skills |
| [plugins.json](plugins.json) | 共通プラグインとアプリ付属の設定 |
| [notify.py](notify.py) | ntfy通知 |

一覧と取得元は [Skills](docs/skills.md)・[プラグイン](docs/plugins.md) を参照してください。各Skillが使うCLIや `codegraph` は別途導入してください。

公開Skillsを追加するには `skills/requirements.json` に名前と取得元を追記し、`./install.sh` を実行します。プラグインの一覧を保存・確認する場合は次のコマンドを使います。

```sh
python3 manage.py snapshot-plugins  # 現在の一覧をplugins.jsonに保存
python3 manage.py check-plugins     # 共通プラグインの導入状態と、その環境のアプリ付属設定を確認
```

`snapshot-plugins` の実行後は `git diff -- plugins.json` を確認してください。他の環境向けのアプリ付属設定は保持します。両コマンドとも `--codex-home` に対応しています。

## 既存設定とバックアップ

- `config.toml` と `AGENTS.md` は置き換えます。変更前のファイルと同名Skillsは `$CODEX_HOME/backups/codex-config/<日時>/` に退避します。
- 公開Skillsはコピーします。自作Skillsと `notify.py` はmacOS・Linux・WSLではリンク、Windowsではコピーします。リンクを使う環境でリポジトリを移動したら再実行してください。
- 認証情報、会話履歴、一覧外のSkillsは変更しません。一覧外のプラグインも削除しませんが、設定ファイル内の個別設定は引き継ぎません。
- プラグインの更新途中で失敗した場合、導入済みの分は自動で巻き戻しません。原因を解消して再実行してください。

復元する場合はCodexを終了し、復元先にある同名のファイル・ディレクトリ・リンクを外してから、バックアップを元の場所へ戻してください。

## 通知

通知を使う場合は、Codex起動時に環境変数 `NTFY_TOPIC` を設定します。互換用の `CODEX_NTFY_TOPIC` も使えます。どちらも未設定なら送信しません。デスクトップアプリにもこの環境変数を渡してください。

```sh
export NTFY_TOPIC="your-private-codex-topic"
```

メインエージェントの1ターンが終わると、依頼の先頭行と最終回答をntfyへ送信します。

## テスト

```sh
python3 -m unittest discover -s tests -v
```
