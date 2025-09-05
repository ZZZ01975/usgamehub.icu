
# US Game Hub – 项目需求文档 v1
_最后更新：2025-09-05_

## 1. 背景与角色
- **项目发起人（你）**  
  - 不懂英文、不懂编程，但想快速上线多个小游戏站。  
  - 目标：先做 1 个 MVP，跑通“发现热词 → 选游戏 → 自动上架 → 基础运营”完整流程，再复制到 5–10 个站。  
- **协作 AI**  
  1. **ChatGPT（Planner）** – 写需求、拆任务、把关质量  
  2. **Claude Code（Builder）** – 生成/修改代码、执行脚本  
  3. **GitHub Actions（Monitor）** – 自动跑测试、失败回写任务  
- **站点目标用户**：18–34 岁、男女比例约 5:5 的轻量游戏玩家（欧美、南美、日韩等英语/非英语地区均覆盖）

## 2. 项目目标
1. **功能 MVP**：  
   - 首页、分类页、游戏详情页均可访问并渲染。  
   - 至少 20 款可玩的 HTML5 游戏。  
2. **全自动内容上线**：脚本将新游戏写入 `data/games.json`、触发 CI 部署。  
3. **最小运营闭环**：  
   - 每周自动生成新游合集页 + RSS  
   - Cloudflare Analytics / GA 采集访问数据  
4. **错误护栏**：JSON Schema、Playwright E2E、Lighthouse ≥80、iframe 安全检查。

## 3. 需求明细
| 模块 | 核心要点 | 验收 |
|------|----------|------|
| **站点结构** | `index.html` + `game.html?id=<id>` + `/category.html` + `/weekly/` | 通过导航栏互相可达 |
| **导航栏** | 固定顶部、简体中文/English 标签 | 移动端折叠菜单正常 |
| **游戏数据** | `data/games.json` 字段：`id,title,desc,tags,category,cover,url,regionBlock` | JSON Schema 校验通过 |
| **数据加载** | `fetch` 加载 JSON，渲染卡片、详情 | 首屏 LCP ≤ 2.5 s（Lighthouse） |
| **自动脚本** | `fetch_trends.py`,`scrape_itchio.py`,`add_game.py`,`weekly_report.py` | 每日/每周任务 Cron 成功 0 错误 |
| **CI/监控** | `.github/workflows/ci.yml` 跑单测 + 端测 + Lighthouse | 任何 red status 自动回写 Issue |
| **国际化** | 默认 英文 UI，浏览器 `lang`=zh 时切换简中 | 站点 meta 正确 |

## 4. 非功能性
- **SEO**：动态 `<title>`、meta、OG；站点地图 & RSS  
- **安全**：iframe `sandbox`、CSP Header  
- **部署**：GitHub Pages 主站 + Cloudflare Pages 镜像缓存

## 5. 里程碑 & 时间
| 阶段 | 目标 | 负责人 |
|------|------|--------|
| M0 | 需求 & CLAUDE.md 固定 | ChatGPT ✔ |
| M1 | 脚手架 + 护栏通过 | Claude Code (1 d) |
| M2 | 日爬虫 & 自动上架跑通 | Claude Code (2 d) |
| M3 | 周合辑 & RSS | Claude Code (1 d) |
| M4 | 第 1 站正式上线 | 你 (验收) |

## 6. 文档体系
```
/docs/
  PRD.md              # 本文件
  CLAUDE.md           # Claude 行为约束
  tasks.md            # 任务清单，Kiro/Claude 更新
  progress_log.md     # 每次 CI 成败或手动备注
```

## 7. 风险 & 回滚
- **API 变动**：爬虫失败 → CI 报错 → 回滚上一个成功构建
- **iframe 被封**：监控脚本每日检测 + 替换备用源
- **广告联盟审核**：上线后再接入；先确保内容质量与活跃度

_复制本文件保存为 `docs/PRD.md`。_
