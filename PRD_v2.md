
# US Game Hub – 项目需求文档 **v2**
_最后更新：2025-09-05_

> **说明**：v2 在 v1 基础上 **新增 SEO/关键词策略与 Google AdSense 合规要点**（章节 8 & 9），并补充“脚本自动化” Checklist。

---

## 1. 背景与角色
- **项目发起人（你）**  
  - 不懂英文、不懂编程，希望用 AI + 脚本低成本搭建并运营小游戏站。  
  - 先完成 1 个 MVP，后续复制到 5–10 个站。  
- **协作 AI**  
  1. **ChatGPT（Planner）** – 写需求、拆任务、质量把关  
  2. **Claude Code（Builder）** – 生成/修改代码、执行脚本  
  3. **GitHub Actions（Monitor）** – 自动跑测试、失败回写任务  
- **目标玩家**：18–34 岁，男女 5:5，碎片娱乐，主要来自欧美、南美、日韩（英文或多语言）。

---

## 2. 项目目标
1. **功能 MVP**：首页 / 分类 / 详情页可访问并渲染 ≥20 款 HTML5 游戏。  
2. **自动上架**：脚本写入 `data/games.json` → CI 通过 → 自动部署。  
3. **运营闭环**：  
   - 每周自动生成新游合集页 + RSS  
   - Cloudflare Analytics / GA 采集访问数据  
4. **质量护栏**：JSON Schema、Playwright E2E、Lighthouse ≥80、iframe 安全检查。

---

## 3. 功能需求明细
| 模块 | 要点 | 验收 |
|------|------|------|
| **站点结构** | `index.html` `game.html?id=<id>` `/category.html` `/weekly/` | 导航互通，无 404 |
| **导航栏** | 固定顶部，EN/简中自动切换 | 移动端折叠菜单正常 |
| **游戏数据** | `games.json`: id/title/desc/tags/category/cover/url/regionBlock/createdAt | JSON Schema 100% 通过 |
| **数据加载** | fetch 渲染卡片 & 详情 | 首页 LCP ≤2.5 s |
| **自动脚本** | `fetch_trends.py` `scrape_itchio.py` `add_game.py` `weekly_report.py` | Cron 任务 0 失败 |
| **CI/监控** | `.github/workflows/ci.yml` 跑单测+端测+Lighthouse | 红灯自动回写 Issue |
| **国际化** | 默认 EN，浏览器 zh → 简中 | meta/lang 标记正确 |

---

## 4. 非功能性
- **SEO**：动态 title/meta/OG；sitemap.xml & RSS 更新  
- **安全**：iframe sandbox，CSP header  
- **部署**：GitHub Pages + Cloudflare Pages 镜像

---

## 5. 里程碑
| 阶段 | 目标 | 负责人 |
|------|------|--------|
| M0 | 确认 PRD & CLAUDE.md | ChatGPT ✅ |
| M1 | 脚手架 + 护栏通过 | Claude Code (1 d) |
| M2 | 日爬虫 & 自动上架 | Claude Code (2 d) |
| M3 | 周合辑 & RSS | Claude Code (1 d) |
| M4 | 第 1 站上线 | 你（验收） |

---

## 6. 文档体系
```
/docs/
  PRD.md         # 本文件
  CLAUDE.md      # Claude 行为约束
  tasks.md       # 任务清单
  progress_log.md
```

---

## 7. 风险与回滚
- **API 变动**：爬虫失败 ➜ CI 报错 ➜ 回滚上一次绿灯构建  
- **iframe 封锁**：每日监控，自动标记 `regionBlock`  
- **AdSense 审核**：上线后再接入；先保证内容/留存/更新

---

## 8. SEO & 关键词策略（热词体系）
| 关键词层 | 定义 | 发现方法 | 示例 |
|-----------|------|----------|------|
| **Evergreen** | 长尾常绿，5 年流量不衰 | `idle`, `solitaire`, `.io game` | “idle farming game online” |
| **Rising** | 近 90 天缓升，KD*<30* | Google Trends + Ahrefs ↗ | “unofficial pokemon browser” |
| **Spike** | <14 天爆红 | Reddit Hot / Twitter Trends | “onlyup browser demo” |

> **脚本**：  
> - `fetch_trends.py`：Google Trends API 拉 Rising & Spike；  
> - `scrape_itchio.py`：抓 itch.io / Steam Upcoming 带 Web demo 游戏；  
> - `match_keywords.py`：关键词 ↔ 游戏标题/标签匹配，输出候选。

**选品原则**  
1. **iframe 可嵌** (无 X-Frame-Options)  
2. **RegionBlock** 字段标记 CN 屏蔽需求  
3. 同关键词只保留 1–2 款，避免内耗。

---

## 9. Google AdSense 合规要点
| 维度 | 要求 | 实现 |
|------|------|------|
| **内容安全** | 无成人、赌博、血腥 | 爬虫黑名单 + 人工 5 min 审核 |
| **用户价值** | 停留 & 页面深度 | - 详情页“30 s 攻略”<br>- 相关推荐 6 条 |
| **持续更新** | 每周 RSS & 合集页 | `weekly_report.py` 自动生成 |
| **站点表现** | CLS<0.1  LCP≤2.5 s | Lighthouse CI 护栏 |
| **政策合规** | 隐私政策 & Cookie 提示 | `/legal/privacy.html` & 简易 Banner |

---

## 10. 自动化脚本 Checklist
- [ ] `fetch_trends.py` → 输出 `hot_keywords.json`
- [ ] `scrape_itchio.py` → 输出 `new_games_raw.csv`
- [ ] `match_keywords.py` → 生成 `candidate_pairs.csv`
- [ ] `add_game.py` → 写入 `data/games.json` + PR
- [ ] `weekly_report.py` → 生成 `/weekly/YYYY-Wk.html` + RSS Ping
- [ ] CI 绿灯：JSON Schema + Playwright + Lighthouse

---

## 11. 版本历史
| 版本 | 日期 | 变动 |
|------|------|------|
| v1 | 2025‑08‑15 | 初版：功能 & 流程 |
| **v2** | 2025-09-05 | 加入 SEO & AdSense 策略章节 |

---

_保存此文件为 `docs/PRD.md` 并提交。_
