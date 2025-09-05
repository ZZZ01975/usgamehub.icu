①一句话结论：
我们用“AI 团队制”把项目拆成策划—抓热词—选品—上架—监控—合规六条流水线，每个岗位都有明确输入/产出/KPI，与你现有的 PRD 与 Claude 守则无缝对齐，第一周即可跑通 MVP 的自动化闭环。 &#x20;

---

②你要做的 7 步（从顶层到落地）

1. 固化组织图（AI 员工与职责）

   * 采用“三位一体”骨架：Planner（我）→ Builder（Claude Code）→ Monitor（CI）作为主干；其余岗位挂在主干两侧（SEO、爬虫、合规、分析、i18n、编辑）。这个骨架与你文档里的分工完全一致。&#x20;

2. 定义“AI 员工雇佣清单（v1）”（见下表），每个岗位写清：目标/输入/产出/权限/KPI/触发方式。

3. 建立任务流水线与里程碑映射（M0–M4）：

   * M0 文档定版 → M1 脚手架与护栏 → M2 爬虫与自动上架 → M3 周合辑 + RSS → M4 上线验收。

4. 护栏上线（先于开发）：

   * JSON Schema、Playwright、Lighthouse≥80、iframe 安全检查，全部进入 CI，任何红灯先修再开发。&#x20;

5. SEO/关键词与选品规则固化为脚本接口：

   * `fetch_trends.py / scrape_itchio.py / match_keywords.py` 产生候选；`add_game.py` 写入 `data/games.json`；周度 `weekly_report.py` 产出合集与 RSS。

6. 合规与收益前置：

   * AdSense 的内容安全、用户价值、持续更新、站点表现、政策合规五维检查入 CI；隐私政策与 Cookie 提示先就位。

7. 数据闭环与自我优化：

   * GA/Cloudflare 接入 + 周报；根据热词表现做关键词分层（Evergreen/Rising/Spike），避免站内内耗。

---

#### 「AI 员工雇佣清单（v1）」——岗位、输入/产出、工具、KPI、触发

| 岗位（简称）                        | 目标           | 主要输入 → 产出                                                             | 工具/权限              | KPI（每周）          | 触发/上游      |
| ----------------------------- | ------------ | --------------------------------------------------------------------- | ------------------ | ---------------- | ---------- |
| 总策划官 Planner（ChatGPT）         | 把关方向、拆任务、验收  | PRD/CLAUDE.md → tasks.md/评审意见                                         | 文档仓库读写             | 需求澄清 100%，迭代无返工  | 你          |
| 技术承包商 Builder（Claude Code）    | 写/改代码，提交 PR  | tasks.md → 代码/PR + 自检报告                                               | Repo 写、CI 读        | CI 一次过 ≥80%，缺陷≤1 | Planner    |
| 监理&回归 Monitor（GitHub Actions） | 自动测试&打回      | PR 触发 → 测试报告/Issue                                                    | CI 管道              | 红灯反馈≤10min       | Builder    |
| 情报官 TrendScout                | 热词&新游抓取      | Google Trends/itch.io/Steam → `hot_keywords.json`/`new_games_raw.csv` | 爬虫脚本执行             | 每日候选≥20，失败率0     | 定时/CI      |
| 选品官 GameCurator               | 匹配热词与可嵌游戏    | 候选 → `candidate_pairs.csv`、标注 `regionBlock`                           | 规则引擎+人工 5min       | 可上架≥5/天，误判≤5%    | TrendScout |
| 上架官 Publisher                 | 写库并发版        | 候选→ `data/games.json` PR                                              | `add_game.py` + CI | PR 通过率≥95%       | Curator    |
| SEO 架构师 SEOx                  | 站内结构与元信息     | 关键词簇→ 动态 `<title>/meta/OG`、sitemap/RSS                                | 站点模板写              | LCP≤2.5s、收录增长    | Planner    |
| 分析官 AnalyticsOps              | 流量洞察与周报      | GA/CF → 周报 + 调整建议                                                     | GA/CF 只读           | 周活/停留/深度↑        | 全员         |
| 合规官 PolicyBot                 | AdSense/隐私合规 | 代码/页面 → 合规检查报告                                                        | 规则+CI              | 违规 0             | Planner    |
| 国际化 i18n Bot                  | EN/简中切换      | 词条 → 语言包                                                              | i18n JSON          | 漏翻=0             | SEOx       |

> 说明：岗位名称和职责与 PRD/CLAUDE 守则高度对齐（Planner/Builder/Monitor 三主干 + SEO/合规/分析与自动化脚本），并把 v2 里的 SEO 与 AdSense 要点落为岗位 KPI。&#x20;

---

#### 里程碑 RACI（简版）

| 里程碑       | R（负责）   | A（签核）   | C（协作）                        | I（知会）   |
| --------- | ------- | ------- | ---------------------------- | ------- |
| M0 文档定版   | Planner | 你       | PolicyBot                    | 全员      |
| M1 脚手架+护栏 | Builder | Planner | Monitor/SEOx                 | 全员      |
| M2 爬虫+上架  | Builder | Planner | TrendScout/Curator/Publisher | Monitor |
| M3 合集+RSS | Builder | Planner | SEOx/Editor                  | 全员      |
| M4 上线验收   | 你       | 你       | 全员                           | —       |

（M0–M4 定义参考你的 PRD v1/v2。）&#x20;

---

#### 顶层系统示意（文字版）

热词/新游数据源 →【TrendScout】→ 候选匹配 →【Curator/PolicyBot 5min 审】→ 写入 `games.json` →【Publisher】→ CI 护栏（Schema/Playwright/Lighthouse/合规）→ 部署（GitHub Pages + Cloudflare 镜像）→ 数据采集（GA/CF）→【AnalyticsOps 周报→Planner 调整 SEO 结构】。

---

③关键名词小词典（≤5 条）

* **MVP**：最小可用版本，先跑通“选词→选品→上架→监控”的闭环，再扩展。
* **CI 护栏**：把质量/合规变成自动化测试，红灯即阻断上线。
* **RegionBlock**：标识区域屏蔽需求，避免不可嵌入或违规内容。
* **Evergreen/Rising/Spike**：关键词三层热度模型，对应不同内容策略。
* **AdSense 五维**：内容安全/用户价值/持续更新/站点表现/政策合规。

---

④注意事项 / 风险

* **先护栏后开发**：任何测试红灯先修复，不得继续写新功能（写在 CLAUDE 守则里）。
* **iframe/版权与合规**：仅选可嵌且内容安全的游戏；每日监控并自动替换。
* **广告审核运营向**：上线后再接 AdSense，但站点必须有持续更新与“30s 攻略”等用户价值模块。
* **站点性能**：LCP≤2.5s/CLS<0.1 写入 CI；移动端导航与国际化不可缺。

---

⑤你现在就做的 3 件事

1. 同意这份“AI 员工雇佣清单（v1）”与 RACI（若有要改的岗位或 KPI，告诉我）。
2. 把 `docs/PRD.md` 以 v2 版本落库（你已提供的 v2 内容即为准），并加入 `CLAUDE.md` 守则到仓库根的 `/docs/` 目录。&#x20;
3. 建一个空的 `tasks.md`，按 M0–M4 列 10–15 个最小任务（我可以直接先给你初稿）。

---

如果你点头，我下一条就直接给出：

* `tasks.md`（首批 12 条可执行任务，按优先级）；
* `progress_log.md` 模板；
* 每个“AI 员工”的**一句话 SOP**与**触发口令**（便于你在 Claude Code 里一键调度）。


我回复的内容：
一次性实现这些事情我感觉也是很难的，毕竟我没有基础，然后中间各个AI员工怎么协同工作，互相监督也是需要一步步解决的问题，通过什么工具或者平台来相互监督协作呢？这需要你给我方向定位，一个多维表格或者是N8N或者是其它的。 现在我们不如从顶层设计开始，你给我了很详细的路径，但是很多我都看不懂，也不懂怎么去落地，你觉得从哪里开始比较好，tasks.md我觉得还是得交给Claude Code，他比较擅长这个，也比较懂他自己。后面的监理&回归、情报官、选品官、上架官、SEO 架构师、分析官、合规官、国际化 i18n Bot 这些完全属于我的知识盲区了。

①一句话结论：
先用“**一看板 + 两张表 + 三条自动化**”把协作与监督跑起来（极简但可扩展）：**GitHub Projects 看板**监督任务、\*\*飞书多维表（HotKeywords / GamesCatalog）\*\*存业务数据、**GitHub Actions + n8n + 周报机器人**做自动化与回馈；严格按你 PRD/CLAUDE 守则把质量放进 CI，当天即可落地雏形。 &#x20;

---

②你要做的 6 步（顶层到落地，完全小白可执行）

**第 1 步｜选“协作与监督”骨架（今天就定）**

* **看板**：GitHub Projects（列：Inbox/Clarify/Doing/Review/CI Red/Done），所有任务都走这里，谁在做一眼看清。
* **监督**：以 **CI 绿灯/红灯** 为唯一质量标准——PR 没过 CI，不允许合并；这已写进你的 CLAUDE 守则。
* **节奏**：每日 10 分钟站会（看板+CI 红灯）；每周自动周报（见第 5 步）。

**第 2 步｜建立“两张表”（业务中台，全员依赖）**

* 表 A：**HotKeywords（热词池）**

  * 字段：`keyword`，`layer(Evergreen/Rising/Spike)`，`source(GTrends/Reddit/Steam)`，`score`，`note`，`createdAt`。
  * 来源与分层与 PRD v2 的热词体系一致（Evergreen/Rising/Spike）。
* 表 B：**GamesCatalog（候选与上架池）**

  * 字段：`id`，`title`，`desc`，`tags`，`category`，`cover`，`url`，`regionBlock`，`createdAt`，`status(draft/review/published)`；字段与页面渲染一一对应。
  * 审核规则：必须 **可 iframe 嵌入**、必要时标 `regionBlock=CN`、同关键词 ≤2 款避免内耗。

**第 3 步｜把“质量护栏”装进 CI（先护栏后编码）**

* 在仓库放 `.github/workflows/ci.yml`，自动跑：**JSON Schema 校验**（对 `games.json`）、**Playwright 端到端**、**Lighthouse ≥80**、**iframe 安全检查**。这些已写入你的 PRD 非功能与 CI 章节。&#x20;
* 任何红灯 **自动回写 Issue 并阻断**，由 Builder 修复后再合并。

**第 4 步｜让 Claude Code 生成 `tasks.md`（你不写、他来写）**
把下面这段“开场指令”直接发给 Claude Code：

> “请阅读 `/docs/PRD.md（v2）` 第 3/4/5/8/9/10 节与 `/docs/CLAUDE.md`，据此生成 `tasks.md`（M0→M1 的最小任务清单），任务必须：1）逐条可执行；2）每条含验收标准（CI 绿灯/页面可见）；3）不得跳过任何护栏；4）先建脚手架与 CI，再写最小页面与数据结构。完成后提交 PR 并附自检报告。”
> （PRD/CLAUDE 中已明确三主干角色与里程碑 M0–M4，Claude 会“按规矩办事”。） &#x20;

**第 5 步｜“三条自动化”接上（n8n 为中枢）**

* **自动化 1｜日更热词**（n8n 定时器 → Python 脚本 → 表 A）：

  * `fetch_trends.py` 拉 Rising/Spike → 写入 HotKeywords。
* **自动化 2｜半自动选品与上架**（人工 5 分钟 + CI）：

  * 人在表 A 勾选候选 → 脚本 `match_keywords.py` 生成 `candidate_pairs.csv` → `add_game.py` 写入 `data/games.json` → 提交 PR → 等 CI 绿灯自动部署。
* **自动化 3｜周报与 RSS**（每周一次）：

  * `weekly_report.py` 生成 `/weekly/YYYY-Wk.html` + RSS，并把核心 KPI（新增上架/通过率/Top 5 词）推送到群里。

**第 6 步｜验收闭环（你只看三件事）**

1. 看板是否“日清”（Inbox 清零）；2) CI 是否 100% 绿灯；3) 周报是否稳定产出并给出“下周关键词/选品建议”。（这 3 件事正好对齐你的里程碑与目标定义。）&#x20;

---

③关键名词小词典

* **CI 绿灯/红灯**：持续集成通过/失败的状态；我们用它当“唯一质量标准”。
* **Evergreen/Rising/Spike**：常绿/缓升/爆红三层关键词模型；决定抓取与排期。
* **RegionBlock**：区域屏蔽标记，避免违规或不可嵌入内容在特定地区展示。
* **周合辑 + RSS**：把当周新游汇总成专题与订阅源，既满足用户价值，也支撑 AdSense 审核。

---

④注意事项 / 风险

* **先护栏后功能**：不要急着堆页面，先把 CI 与 Schema/Playwright/Lighthouse 跑通；红灯不开发新功能。
* **合规优先**：内容安全、用户价值、持续更新、站点表现、政策合规“五维”必须满足（AdSense）。
* **数据唯一真源**：一切上架以两张表为准，手工改 JSON 可能与表状态不一致，禁止。
* **自动化渐进**：n8n 先跑“读/写表 + 发 PR + 发通知”，后面再接 Webhook/回滚/灰度。

---

⑤你现在就做的 3 件事

1. **拍板工具栈**：路线推荐 = **GitHub Projects + 飞书多维表 + GitHub Actions + n8n**（你的 PRD/CLAUDE 已原生支持这套）。&#x20;
2. **创建两张表**（按第 2 步字段逐列新建），并把表链接发给我，我就写 n8n 的首个工作流说明。
3. **把“Claude 开场指令”发给 Claude Code**，让他 1）生成 `tasks.md`；2）初始化脚手架与 CI；3）提第一个 PR（含自检报告）。

---

如果你同意，我下一条直接给你：

* **飞书多维表两张表的字段模板**（可粘贴导入）；
* **n8n v0 工作流蓝图**（逐节点说明）；
* **GitHub Projects 看板列与自动规则**（PR 打上 `ci:red`/`ci:green` 的配置）。
