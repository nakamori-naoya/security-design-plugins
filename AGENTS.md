> 共通の規約は /Users/naoya-nakamoriq/Documents/Github/harness-pluginsv2/AGENTS.md にある。ここには、この repository だけの規則を置く。

# security-design

公開・インストール対象は package `security-design@security-design`（`./plugins/security-design`）一件で、公開入口は五つ、内部 skill は置かない。

- `decide-what-to-protect` は、何を、誰から、どこまで守るかを決める。ほかの四つの入口は、この入口が保存した資料を入力に受け取り、守るものを自分で決め直さない。
- `analyze-browser-security`、`analyze-server-security`、`analyze-infrastructure-security` は、それぞれの層で、守るものへ届く攻撃の経路と対策を分析する。層の分け方は攻撃が通る場所で決め、どの層にも属する脅威は、その脅威を最後に止める層が持つ。
- `design-security` は playbook で、上の四つを順に呼び、層をまたぐ脅威と、層どうしが互いに相手が守ると思い込んだ隙間を見つけ、公開前に入れる対策を一本の資料にまとめる。各層の判断を書き直さない。

費用、残すリスクの受け入れ、守る範囲の線引きは利用者が決めることで、どの入口も grill の公開入口で問う。資料は write-doc の公開入口で保存する。入口ごとの外部 entry point の保護の宣言は development-convention の `protect-entry-points` が持ち、この package は宣言の中身を書き直さない。

案件固有の値（特定のクラウドの製品名、閾値、料金）を、規約や判断例の正解にしない。
