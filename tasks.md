# US Game Hub MVP - 任务清单

> 基于 PRD_v2.md 和 CLAUDE.md 规则制定  
> 严格按照次序执行，完成一项即勾选并记录

---

## 📋 阶段一：游戏数据准备 (M1)

### 任务 1.1：数据结构设计
- [ ] **1.1.1** 创建 `data/` 目录结构
- [ ] **1.1.2** 设计 `data/games.json` 数据模型
- [ ] **1.1.3** 创建 `data/game-schema.json` JSON Schema 验证
- [ ] **1.1.4** 创建 `data/categories.json` 分类数据

**验收标准**：JSON Schema 校验 100% 通过

---

### 任务 1.2：30 个种子游戏数据生成

#### 益智类游戏 (10个) - 长尾SEO优化
- [ ] **1.2.1** 2048 Game - 关键词: "play 2048 game online free"
- [ ] **1.2.2** Tetris Classic - 关键词: "tetris online no download"
- [ ] **1.2.3** Sudoku Puzzle - 关键词: "sudoku puzzle easy medium hard"
- [ ] **1.2.4** Minesweeper - 关键词: "minesweeper classic online"
- [ ] **1.2.5** Mahjong Connect - 关键词: "mahjong connect free games"
- [ ] **1.2.6** Bubble Shooter - 关键词: "bubble shooter classic free"
- [ ] **1.2.7** Zuma Deluxe - 关键词: "zuma deluxe online play"
- [ ] **1.2.8** Match 3 Puzzle - 关键词: "match 3 puzzle games"
- [ ] **1.2.9** Jigsaw Puzzles - 关键词: "jigsaw puzzles online free"
- [ ] **1.2.10** Memory Game - 关键词: "memory card matching game"

#### 动作类游戏 (10个) - 热门关键词
- [ ] **1.2.11** Endless Runner - 关键词: "endless runner games 3d"
- [ ] **1.2.12** Stickman Fighter - 关键词: "stickman fighting games 2 player"
- [ ] **1.2.13** Tank Battle - 关键词: "tank battle multiplayer online"
- [ ] **1.2.14** Air Combat - 关键词: "airplane shooting games free"
- [ ] **1.2.15** Ninja Run - 关键词: "ninja run jump game"
- [ ] **1.2.16** Zombie Survival - 关键词: "zombie survival games browser"
- [ ] **1.2.17** Racing Car - 关键词: "car racing games unblocked"
- [ ] **1.2.18** Platform Jump - 关键词: "platform jumping games"
- [ ] **1.2.19** Space Shooter - 关键词: "space shooter retro arcade"
- [ ] **1.2.20** Archery Master - 关键词: "archery bow arrow games"

#### 双人游戏 (5个) - 社交关键词
- [ ] **1.2.21** Tic Tac Toe - 关键词: "tic tac toe 2 player"
- [ ] **1.2.22** Gomoku Online - 关键词: "gomoku online with friend"
- [ ] **1.2.23** Tank Duo - 关键词: "2 player tank games same keyboard"
- [ ] **1.2.24** Soccer Heads - 关键词: "soccer games 2 player local"
- [ ] **1.2.25** Racing Rivals - 关键词: "racing games split screen"

#### 棋牌类游戏 (5个) - 经典关键词
- [ ] **1.2.26** Solitaire Classic - 关键词: "solitaire card games free"
- [ ] **1.2.27** FreeCell - 关键词: "freecell solitaire online"
- [ ] **1.2.28** Spider Solitaire - 关键词: "spider solitaire 2 suits"
- [ ] **1.2.29** Chess Master - 关键词: "chess online vs computer"
- [ ] **1.2.30** Checkers Game - 关键词: "checkers board game online"

**验收标准**：
- 每个游戏包含 200-300 字 SEO 优化描述
- 确保 iframe 可嵌入（测试后确认）
- 分类和标签正确归属

---

## 🏗️ 阶段二：项目基础架构 (M1-M2)

### 任务 2.1：目录结构创建
- [ ] **2.1.1** 创建根目录文件结构
```
/
├── index.html          # 首页
├── game.html          # 游戏详情页
├── category.html      # 分类页
├── search.html        # 搜索页
├── about.html         # 关于页
├── privacy.html       # 隐私政策
├── sitemap.xml        # SEO 站点地图
├── robots.txt         # 爬虫规则
└── manifest.json      # PWA 配置
```

- [ ] **2.1.2** 创建 `/css/` 样式目录
```
/css/
├── main.css           # 主样式文件
├── responsive.css     # 响应式样式
└── components.css     # 组件样式
```

- [ ] **2.1.3** 创建 `/js/` 脚本目录
```
/js/
├── app.js            # 主应用逻辑
├── games.js          # 游戏加载管理
├── analytics.js      # Google Analytics
└── utils.js          # 工具函数
```

- [ ] **2.1.4** 创建 `/assets/` 资源目录
```
/assets/
├── /images/          # 游戏缩略图
├── /icons/           # 分类图标
└── /logos/           # 网站Logo
```

**验收标准**：目录结构完整，文件路径规范

---

### 任务 2.2：技术配置
- [ ] **2.2.1** 配置 `.github/workflows/ci.yml` GitHub Actions
  - JSON Schema 验证
  - Lighthouse CI（目标 ≥80）
  - 自动部署到 Cloudflare Pages
- [ ] **2.2.2** 配置 Google Analytics 4
- [ ] **2.2.3** 配置 Cloudflare Analytics
- [ ] **2.2.4** 设置 iframe 安全检查
- [ ] **2.2.5** 创建 `robots.txt` 和 `sitemap.xml` 模板

**验收标准**：CI 流水线 100% 绿灯通过

---

## 🎨 阶段三：页面设计实现 (M2-M3)

### 任务 3.1：首页设计 (index.html)
- [ ] **3.1.1** 顶部导航栏设计
  - 固定定位，响应式布局
  - Logo + 站点标题
  - 搜索框（实时过滤）
  - 分类下拉菜单
  - EN/简中语言切换

- [ ] **3.1.2** Hero 轮播区域
  - 5个热门游戏轮播展示
  - 自动播放，5秒切换
  - 点击进入游戏详情

- [ ] **3.1.3** 分类导航网格
  - 6个主要分类（益智、动作、双人、棋牌、体育、其他）
  - 图标 + 文字描述
  - 悬停动效

- [ ] **3.1.4** 游戏展示区域
  - "最新游戏" 2行×4列 = 8个
  - "热门游戏" 3行×4列 = 12个
  - 卡片式设计，含缩略图、标题、简介

- [ ] **3.1.5** 页面底部
  - 热门标签云（SEO 优化）
  - 友情链接位置
  - 版权信息和隐私政策链接

**验收标准**：
- 移动端完美适配
- 首屏加载时间 < 3秒
- 符合 CrazyGames/Poki 设计风格

---

### 任务 3.2：游戏详情页 (game.html)
- [ ] **3.2.1** 页面头部
  - 面包屑导航（首页 > 分类 > 游戏名）
  - 游戏标题和描述
  - 分享按钮组

- [ ] **3.2.2** 游戏主体区域
  - iframe 游戏容器（16:9 比例）
  - 全屏播放按钮
  - 加载动画效果

- [ ] **3.2.3** 游戏信息区域
  - 详细游戏描述（200-300字，SEO优化）
  - 操作说明和游戏攻略
  - 游戏标签和分类
  - 评分系统和播放次数

- [ ] **3.2.4** 相关推荐区域
  - "相似游戏推荐" 8个
  - "同分类热门" 4个
  - 智能推荐算法

**验收标准**：
- 游戏加载流畅无卡顿
- SEO 元数据动态生成
- 用户停留时间 > 2分钟

---

### 任务 3.3：分类和搜索页面
- [ ] **3.3.1** 分类页面 (category.html)
  - 分类标题和描述
  - 游戏筛选和排序
  - 分页加载功能

- [ ] **3.3.2** 搜索页面 (search.html)
  - 实时搜索结果
  - 搜索历史记录
  - 热门搜索词推荐

- [ ] **3.3.3** 静态页面
  - 关于我们页面
  - 隐私政策页面
  - Cookie 使用说明

**验收标准**：所有页面导航互通，无404错误

---

## ⚡ 阶段四：性能优化 (M3-M4)

### 任务 4.1：性能优化
- [ ] **4.1.1** 图片懒加载实现
- [ ] **4.1.2** CSS/JS 文件压缩
- [ ] **4.1.3** 缓存策略配置
- [ ] **4.1.4** PWA 支持添加
- [ ] **4.1.5** 确保 Lighthouse 得分 ≥ 80

### 任务 4.2：SEO 优化
- [ ] **4.2.1** 每页独特的 title/meta 标签
- [ ] **4.2.2** Open Graph 和 Twitter 卡片
- [ ] **4.2.3** 结构化数据标记
- [ ] **4.2.4** 自动生成 sitemap.xml
- [ ] **4.2.5** Google Search Console 提交

### 任务 4.3：AdSense 准备
- [ ] **4.3.1** 内容质量检查（原创性、价值性）
- [ ] **4.3.2** 用户体验优化（停留时间、点击深度）
- [ ] **4.3.3** 合规检查（隐私政策、Cookie 提示）
- [ ] **4.3.4** 提交 Google AdSense 审核

**最终验收标准**：
- CI 流水线 100% 绿灯
- Lighthouse 性能/SEO/无障碍/最佳实践 均 ≥ 80
- 30 个游戏全部可正常运行
- AdSense 政策合规

---

## 📊 执行规则

### 任务执行顺序
1. 严格按照编号顺序执行
2. 当前任务未完成不得开始下一任务
3. 每完成一个子任务立即勾选
4. CI 红灯必须修复后才能继续

### 验收要求
- 每个任务完成后运行相关测试
- 在 `progress_log.md` 中记录进度
- PR 必须包含自检报告
- 代码质量必须通过 CI 检查

### 紧急澄清机制
如遇需求不明，在对应任务下注释 `Clarify: [具体问题]` 并暂停，等待 Planner 回复。

---

**执行者：Claude Code**  
**监督者：GitHub Actions CI**  
**验收者：项目发起人**  

_最后更新：2025-09-05_