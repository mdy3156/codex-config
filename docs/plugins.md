# プラグイン

`plugins.json` で共通プラグインとアプリ付属の設定を管理します。

- `plugins`：全環境で導入する14個。Git・リモート配信から公式CLIで取得します。
- `app_plugins`：アプリ付属11件の有効状態。OS・アプリのバージョンごとに、提供されるものへ適用します。
- `marketplaces`：取得元の種類。アプリ付属の絶対パスは各環境で検出し、Gitには記録しません。

## 導入・更新

共通プラグインは次の順で更新します。

1. Gitマーケットプレイスを登録し、`codex plugin marketplace upgrade <名前>` でカタログを更新します。現在の2個は `main` を追います。
2. 共通プラグイン全件へ `codex plugin add <ID>` を実行します。同じバージョン番号でも取得し直します。
3. 記録した有効状態を適用し、共通プラグイン全件の導入状態を確認します。不足・有効状態の不一致・取得失敗があればエラーにします。

古いコミット固定とブランチ指定が衝突する場合は、公式CLIで該当マーケットプレイスを登録し直します。バージョンやコミットは固定せず、実行時に配布される版を使います。

## アプリ付属の設定

`openai-bundled`・`openai-primary-runtime` は、アプリ・実行環境が提供するカタログです。Windows/macOSのアプリを一度起動し、そのOS側で導入スクリプトを実行してください。

スクリプトは導入先のカタログを読み、`app_plugins` に記録した有効状態を、その環境で提供されるプラグインに設定します。カタログがない環境や、現在のアプリで提供されない項目は、別環境向けの設定として残します。WSLからWindows用の実行ファイルやカタログをコピーすることはありません。

アプリ付属の本体と実行環境はアプリが管理します。共通プラグインのようにCLIから再インストールする対象にはしません。スクリプトの結果は「共通プラグインの導入確認」と「アプリ付属の設定確認」を分けて表示します。設定の確認はツールの動作確認や外部サービスへの認証を保証するものではありません。

WindowsアプリとWSLのCLIは、既定では別のCodexホームを使います。WindowsではPowerShellから `python manage.py install` / `python manage.py update`、macOS・WSLでは `./install.sh` / `./update.sh` を実行します。各環境にCodex CLIなどの前提ツールが必要です。[WindowsとWSLの公式説明](https://learn.chatgpt.com/docs/windows/windows-app#share-config-auth-and-sessions-with-wsl)も参照してください。

## 記録と確認

```sh
python3 manage.py snapshot-plugins
python3 manage.py check-plugins
```

Windowsでは `python3` を `python` に置き換えてください。両コマンドとも `--codex-home` に対応しています。

`snapshot-plugins` は共通プラグインを現在の導入一覧で更新します。アプリ付属の有効状態も記録しますが、他の環境向けの設定は削除しません。実行後は `git diff -- plugins.json` を確認してください。

`check-plugins` は共通プラグイン全件のID・有効状態と、その環境で適用対象となるアプリ付属設定を確認します。最新版を取得するには `update.sh` を実行してください。

一覧外のプラグインはアンインストールしません。設定全体の置き換えにより、一覧外の個別設定は引き継がれません。途中で更新に失敗した場合、導入済みのプラグインは巻き戻さずエラー終了します。ログイン・外部サービスへの認証・必要な承認は各環境で行ってください。

## 共通プラグイン

| プラグインID | 配布方法 |
| --- | --- |
| `app-69ef18c674308191a2f952431f91ea61@openai-curated-remote` | リモート配信 |
| `codex-security@openai-curated-remote` | リモート配信 |
| `figma@openai-curated-remote` | リモート配信 |
| `github@openai-curated-remote` | リモート配信 |
| `google-calendar@openai-curated-remote` | リモート配信 |
| `google-drive@openai-curated-remote` | リモート配信 |
| `openai-templates@openai-curated-remote` | リモート配信 |
| `pages@openai-curated-remote` | リモート配信 |
| `plugin-creator@openai-curated-remote` | リモート配信 |
| `plugin-management@openai-curated-remote` | リモート配信 |
| `ponytail@ponytail` | Git |
| `sites@openai-curated-remote` | リモート配信 |
| `superpowers@superpowers-dev` | Git |
| `work-pets@openai-curated-remote` | リモート配信 |

`app-69ef18c674308191a2f952431f91ea61` はCLIが返したIDを保存しています。

## アプリ付属の設定一覧

この一覧は全環境で同じ11個を導入するための依存一覧ではありません。カタログに存在する項目へ有効状態を設定するための一覧です。

| プラグインID | 有効状態 |
| --- | --- |
| `browser@openai-bundled` | 有効 |
| `code-review@openai-bundled` | 有効 |
| `codex-app-tools@openai-bundled` | 有効 |
| `computer-use@openai-bundled` | 有効 |
| `documents@openai-primary-runtime` | 有効 |
| `pdf@openai-primary-runtime` | 有効 |
| `presentations@openai-primary-runtime` | 有効 |
| `spreadsheets@openai-primary-runtime` | 有効 |
| `template-creator@openai-primary-runtime` | 有効 |
| `unified-computer-use@openai-bundled` | 有効 |
| `visualize@openai-bundled` | 有効 |

操作方法は [README](../README.md#管理するファイル)、CLIの仕様は [公式リファレンス](https://learn.chatgpt.com/docs/cli/reference#codex-plugin) を参照してください。
