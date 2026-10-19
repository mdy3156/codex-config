# Skills一覧

公開Skillsの本体はリポジトリに含めません。`skills/requirements.json` がSkill名と取得元の一覧です。`install.sh` と `update.sh` はVercelのskills CLIを使い、実行時点の最新版を取得して導入します。

## 公開Skills

| Skills | 公開元 |
| --- | --- |
| defuddle, json-canvas, knap, obsidian-bases, obsidian-cli, obsidian-markdown | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) |
| pdf, playwright, jupyter-notebook | [openai/skills](https://github.com/openai/skills/tree/main/skills/.curated) |
| kaggle-cli | [Kaggle/kaggle-cli](https://github.com/Kaggle/kaggle-cli/tree/main/skills) |
| ml-paper-writing | [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs/tree/main/20-ml-paper-writing/ml-paper-writing) |
| scientific-visualization | [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/scientific-visualization) |
| natural-japanese | [coji/natural-japanese](https://github.com/coji/natural-japanese) |
| yomiyasu | [nanaism/yomiyasu](https://github.com/nanaism/yomiyasu) |
| humanizer | [blader/humanizer](https://github.com/blader/humanizer) |
| proofread | [zmoog/skills](https://github.com/zmoog/skills/tree/main/proofread) |

以前の独自改変版7個は廃止しました。PDF抽出手順、Notebookの出力先処理、科学図版の追加スクリプト、日本語文章規範の分割などのローカル変更は引き継ぎません。今後は公開元の動作・指示をそのまま利用します。

取得するファイルの範囲はskills CLIに従います。各Skillのライセンスは公開元を参照してください。

## ローカル管理

- `latex-documents`：ユーザー固有のLaTeX Workshopレシピと数式番号の規約。

`custom` は作者を断定する分類ではなく、このリポジトリで直接保守するという扱いです。

## Codexが管理するもの

imagegen、openai-docs、skill-creator、skill-installerなどの付属Skillsは、Codex側の管理に任せます。古い `.system/` のコピーは削除しました。プラグインの本体やキャッシュもGitに含めません。

導入先にある、依存一覧にも `custom/` にも含まれないSkillsは変更しません。
