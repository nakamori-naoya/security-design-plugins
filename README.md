# security-design

何を守るかを決めてから、ブラウザ、サーバーサイド、インフラの層ごとに脅威と対策を分析し、公開前に入れる対策を一つの優先順位にまとめる、Claude Code と Codex の両方で使える plugin です。公開するのは `security-design@security-design` の一つの package で、入口は五つあります。

| 入口 | 決めること |
|---|---|
| `design-security` | 通しで進める playbook。下の四つを呼び、層をまたぐ脅威と層どうしの隙間を見つけ、公開前に入れる対策と受け入れたリスクをまとめる |
| `decide-what-to-protect` | 何を（壊されたら困る業務の結果）、誰から（動機と能力）、どこまで（費用の上限、受け入れるリスク、守らないもの）守るか |
| `analyze-browser-security` | ブラウザと利用者の端末を通る攻撃と、その守り |
| `analyze-server-security` | 認可、入力の検証と業務の不変条件、順序と時刻、認証の実装など、サーバーサイドの守り |
| `analyze-infrastructure-security` | 権限と管理の経路、供給経路、費用の攻撃と停止、バックアップ、監視など、インフラと運用の守り |

層の分析は、守るものの資料を入力に取ります。守るものが決まっていない分析は、対策を比べる物差しを持たないからです。費用、残すリスクの受け入れ、守る範囲の線引きは利用者が決めることで、どの入口も grill で問います。資料は write-doc で保存します。

判断の要は、『セキュア・バイ・デザイン』（Dan Bergh Johnsson ほか）の、セキュリティを機能ではなく設計の性質として扱う考え方（ドメインプリミティブ、検証の順序、不変条件、3つの R）と、『サイバーセキュリティの教科書』（Thomas Kranz）の、資産・攻撃者・今ある守りから始めてリスクで優先し、侵害を前提に検知と復旧を備える進め方から取っています。

この plugin は、対策の実装、入口ごとの保護の宣言（development-convention の `protect-entry-points`）、クラウドの製品の選定（system-design の `design-cloud-architecture`）を扱いません。外部の package には、grill と write-doc の公開入口としてだけ依存します。

## 配布構造

Codex の marketplace は `.agents/plugins/marketplace.json`、Claude Code の marketplace は `.claude-plugin/marketplace.json`、配布する package は `plugins/security-design` です。

## 検証

`bash scripts/validate.sh` は、兄弟 checkout の `../harness-tools` による package の構造検査、各入口の SKILL.md の frontmatter と、リンクが自分の入口の中に届くことの検査、その検査の負例の試験を実行します。harness-tools の checkout が無ければ止まります。
