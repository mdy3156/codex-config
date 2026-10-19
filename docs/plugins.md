# プラグイン

`plugins.json` は導入するプラグインと有効状態の一覧です。バージョンやコミットを固定せず、`install.sh` と `update.sh` の実行時に公式CLIで更新します。

## 更新の流れ

1. Gitマーケットプレイスを登録し、`codex plugin marketplace upgrade <名前>` で最新カタログを取得します。現在の2個は `main` を追います。`ref` を省略した取得元は既定ブランチを使います。
2. 全対象へ `codex plugin add <ID>` を実行し、本体を取得し直します。同じバージョン番号でも、取得処理を省略しません。
3. CLIによる導入後に記録した有効・無効状態を適用し、対象がすべて導入済みか確認します。

古いコミット固定と新しいブランチ指定が衝突する場合は、公式CLIで該当マーケットプレイスを登録し直します。独自のカタログ書き換えや、プラグインキャッシュのコピーは行いません。

アプリ付属プラグインは導入先アプリの提供する版、リモート配信プラグインはログイン中のアカウントで提供される版を使います。アプリやCLI自体の更新はこのスクリプトの対象外です。

`check-plugins` は導入済みのIDと有効状態の確認です。最新版を取得するには `update.sh` を実行してください。更新は公開元の配布方針に従います。将来、公開元のカタログが本体の特定版を指定した場合も、そのカタログで提供される版を使います。

## 別環境への反映

追加・削除・有効状態の変更後は `python3.14 manage.py snapshot-plugins` で依存一覧を保存します。バージョン更新だけなら依存一覧の変更は不要です。保存されたGit取得元は既定ブランチに追従します。

認証トークン、外部サービスへの接続情報、アカウント固有のインストールID、プラグインキャッシュはGitに保存しません。新環境ではログイン・再認証・必要な承認を行ってください。サービス側の利用権限も必要です。

依存一覧にない既存プラグインはアンインストールしません。設定全体の置き換えに伴い、一覧外のプラグインの設定は引き継がれません。途中で更新に失敗した場合、すでに導入したプラグインは巻き戻さずエラー終了します。

## 対象一覧

正本は `plugins.json` です。今回取り込んだ26個はすべて有効です。

| プラグインID | 配布方法 |
| --- | --- |
| `app-69ef18c674308191a2f952431f91ea61@openai-curated-remote` | リモート配信 |
| `browser@openai-bundled` | アプリ付属 |
| `code-review@openai-bundled` | アプリ付属 |
| `coderabbit@openai-curated-remote` | リモート配信 |
| `codex-app-tools@openai-bundled` | アプリ付属 |
| `codex-security@openai-curated-remote` | リモート配信 |
| `computer-use@openai-bundled` | アプリ付属 |
| `documents@openai-primary-runtime` | アプリ付属 |
| `figma@openai-curated-remote` | リモート配信 |
| `github@openai-curated-remote` | リモート配信 |
| `google-calendar@openai-curated-remote` | リモート配信 |
| `google-drive@openai-curated-remote` | リモート配信 |
| `openai-templates@openai-curated-remote` | リモート配信 |
| `pages@openai-curated-remote` | リモート配信 |
| `pdf@openai-primary-runtime` | アプリ付属 |
| `plugin-creator@openai-curated-remote` | リモート配信 |
| `plugin-management@openai-curated-remote` | リモート配信 |
| `ponytail@ponytail` | Git |
| `presentations@openai-primary-runtime` | アプリ付属 |
| `sites@openai-curated-remote` | リモート配信 |
| `spreadsheets@openai-primary-runtime` | アプリ付属 |
| `superpowers@superpowers-dev` | Git |
| `template-creator@openai-primary-runtime` | アプリ付属 |
| `unified-computer-use@openai-bundled` | アプリ付属 |
| `visualize@openai-bundled` | アプリ付属 |
| `work-pets@openai-curated-remote` | リモート配信 |

`app-69ef18c674308191a2f952431f91ea61` はCLIが返したIDをそのまま保存しています。

操作方法は [README](../README.md#プラグインの管理)、公式仕様は [Codex CLI](https://learn.chatgpt.com/docs/developer-commands?surface=cli) と [プラグインのマーケットプレイス](https://developers.openai.com/plugins/build/plugins) を参照してください。
