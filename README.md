# codex-config

個人用のCodex設定、自作Skills、プラグイン、ntfy通知を管理します。公開Skillsとプラグインの本体はGitに含めず、取得元と導入するものの一覧を保存します。

**`install.sh` と `update.sh` は、実行するたびに配布元の最新版を取得して適用します。** バックグラウンドでの定期更新や、過去のコミットへの固定は行いません。

## 導入

必要なもの：Git、Python 3.11以降、Node.js 22.20.0以降とnpm、`codex plugin` に対応したCodex CLI。検証したCLIはCodex 0.162.1、Vercel skills 1.7.2です。

先にCodexアプリとCLIを導入し、同じアカウントでログインしてアプリを一度起動してください。現在の26個にはアプリ付属プラグインが含まれるため、全体の再現には対応するアプリ環境が必要です。スクリプト自体はmacOS・Linux・WSL向けです。各Skillが使うCLIと `codegraph` は別途導入してください。

```sh
git clone https://github.com/mdy3156/codex-config.git
cd codex-config
./install.sh --dry-run
./install.sh
```

`python3` が古い環境では `PYTHON=python3.14 ./install.sh` のように指定できます。配置先は `$CODEX_HOME`、未設定なら `~/.codex`。`--codex-home /path/to/codex` でも指定できます。リポジトリは配置先とは別のディレクトリにcloneしてください。

## 更新

```sh
git pull --ff-only  # このリポジトリの設定・依存一覧を更新
./update.sh        # 公開Skills・プラグインの最新版を取得し、設定も適用
```

導入と更新は同じ処理です。どちらも `--dry-run` に対応し、通信・書き込みなしで対象を表示できます。以前の「固定コミットを書き換えてから再導入する」操作は不要です。

最新版を追うため、別の日に実行した環境同士でバージョンが違うことはあります。同じ一覧のSkills・プラグインを、その時点で取得できる版で揃える方針です。アプリ付属プラグインの最新版は、導入先アプリが提供する版です。Codexアプリ・CLI自体の更新は別途行ってください。

## 利用する公開ツール

| 対象 | 使用する仕組み |
| --- | --- |
| 公開Skills | [Vercelのskills CLI](https://github.com/vercel-labs/skills) の `npx --yes skills@latest add` |
| プラグイン | [Codex公式CLI](https://learn.chatgpt.com/docs/cli/reference) の `plugin marketplace add` / `upgrade` と `plugin add` |
| 設定・通知・自作Skills | このリポジトリの配置・バックアップ処理 |

公開ツールをそのまま呼び出し、取得・更新処理を独自に複製しません。Skillsは一時ディレクトリへ取得・検証した後、指定したCodex環境へ配置します。これにより、既存ファイルのバックアップと `$CODEX_HOME` への導入を両立させています。`npx skills update -g` はこのリポジトリの更新手順ではありません。

## 管理するもの

| 場所 | 用途 |
| --- | --- |
| `skills/custom/` | このリポジトリで直接保守するSkills |
| [skills/requirements.json](skills/requirements.json) | 公開Skill名と、skills CLIへ渡す取得元 |
| [plugins.json](plugins.json) | プラグインID、有効状態、マーケットプレイスの取得元 |
| `config.toml` / `notify.py` | 共通設定と通知プログラム |

公開Skillsは13個。以前の独自改変版7個も公開版を使います。出典は [Skills一覧](docs/skills.md) を参照してください。公開Skillの追加は `requirements.json` に名前と取得元を追記して `./install.sh` を実行します。

```json
{
  "skill-name": "https://github.com/owner/repository.git"
}
```

GitHubリポジトリ内の特定フォルダを指定するURLや、公開された `SKILL.md` の直接URLも利用できます。新しい自作Skillは `skills/custom/<名前>/SKILL.md` に作成してください。公開Skillと名前を重複させないでください。

プラグインを追加・削除したり有効状態を変えたりした後は、現在の一覧を保存します。

```sh
python3.14 manage.py snapshot-plugins
git diff -- plugins.json
```

`python3.14 manage.py check-plugins` で、記録したプラグインが導入済みで有効状態も一致するか確認できます。バージョン固定や最新版判定のコマンドではありません。両コマンドは `--codex-home` に対応しています。配布方法と一覧は [プラグイン詳細](docs/plugins.md) を参照してください。

## 既存環境の扱い

- `config.toml` はリポジトリの設定で**全体を置き換えます**。通知のパスと、プラグイン・マーケットプレイスの設定は導入時に生成します。
- 公開Skillsは `$CODEX_HOME/skills/<名前>/` にコピーし、自作Skillsと `notify.py` はリポジトリへのリンクにします。リポジトリを移動したら再導入してください。
- 変更前の設定・同名Skillは `$CODEX_HOME/backups/codex-config/<日時>/` に退避します。内容が同じなら再配置しません。
- アプリ付属マーケットプレイスの確認と全公開Skillsの取得・検証が終わるまで、既存の設定は変更しません。
- 設定とSkillsの配置後にプラグインを更新します。途中で失敗した場合はエラー終了します。原因を解消して再実行してください。導入済みプラグインは自動で巻き戻しません。
- 一覧にないSkills、認証情報、会話履歴は変更しません。一覧にないプラグインはアンインストールしませんが、設定全体の置き換えにより個別設定は引き継がれません。

マシン固有の絶対パス、プロジェクトの信頼設定、フック承認履歴、`rules/` の環境固有のコマンド許可は導入対象外です。各環境でログイン・外部サービスへの再認証・必要な承認を行ってください。

復元する場合はCodexを終了し、表示されたバックアップ内のファイルを元の場所に戻します。導入後の同名ディレクトリやリンクを先に外してから、退避したディレクトリを戻してください。

## 通知

タイトルは `codex-config｜完了：通知タイトルを改善して` のように、作業ディレクトリ名と最後の依頼の先頭行を使います。依頼文がなければ最終回答、それもなければ「ターン完了」を使い、100文字以内に収めます。本文は最終回答です。ここでいう完了はCodexの1ターンの完了です。

サブエージェントの完了は通知しません。メタデータを確認できなければ、メイン通知を取りこぼさないよう送信します。

```sh
python3 notify.py --dry-run '{"type":"agent-turn-complete","cwd":"/work/codex-config","input-messages":["通知タイトルを改善して"],"last-assistant-message":"通知を改善しました。"}'
```

送信先は既存のntfyトピックを引き継ぎます。Codex起動時の `CODEX_NTFY_TOPIC` 環境変数で変更できます。依頼の先頭行と最終回答はntfyへ送信されます。

通知フィールドは [Codexの公式仕様](https://learn.chatgpt.com/docs/config-file/config-advanced)、日本語タイトルの送信形式は [ntfyのJSON API](https://docs.ntfy.sh/publish/#publish-as-json) に従っています。

## 検証

```sh
python3.14 -m unittest discover -s tests -v
```

テストは一時ディレクトリとCLIの代替処理を使い、更新の適用、公開版への置き換え、バックアップ、再実行、取得失敗時の保護、プラグインの記録・照合、通知内容を検証します。普段の設定の変更やntfyへの実送信は行いません。
