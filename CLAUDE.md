# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个免费在线游戏网站项目 (GameVault/US Game Hub)，使用纯静态 HTML/CSS/JavaScript 构建，部署到 Cloudflare Pages。项目遵循严格的任务驱动开发流程。

## 核心规则

1. **语言要求**：所有输出必须使用**简体中文**
2. **任务执行**：严格按照 `tasks.md` 中的任务顺序执行，完成一项即勾选并记录
3. **文件权限**：只能修改 tasks.md 中明确指定的文件，不得随意创建新文件
4. **CI 优先**：发现 CI 报错必须立即停止新功能开发，先修复至通过

## 开发命令

### 数据验证
```bash
# JSON Schema 验证
ajv validate -s data/game-schema.json -d data/games.json

# HTML 验证 
html-validate index.html game.html category.html privacy.html
```

### 性能测试
```bash
# Lighthouse CI 本地运行
npm install -g @lhci/cli
lhci autorun --config .lighthouserc.json

# 性能要求：所有指标 ≥ 80 分
```

### 安全检查
```bash
# 检查敏感信息
grep -r -i "api[_-]key\|password\|secret\|token" --exclude-dir=.git .

# iframe 安全检查
grep -r "sandbox=" *.html
```

### 部署
- 自动部署：推送到 main 分支触发 GitHub Actions
- 目标平台：Cloudflare Pages
- 域名：usgamehub.icu

## 项目架构

### 目录结构
```
/
├── data/                    # 游戏数据和配置
│   ├── games.json          # 主游戏数据库
│   ├── categories.json     # 分类定义
│   └── game-schema.json    # JSON Schema 验证规则
├── css/                    # 样式文件
│   ├── main.css           # 主样式
│   ├── responsive.css     # 响应式设计
│   └── components.css     # 组件样式
├── js/                     # JavaScript 模块
│   ├── app.js             # 主应用逻辑
│   ├── games.js           # 游戏加载管理
│   ├── i18n.js            # 多语言支持
│   ├── utils.js           # 工具函数
│   └── analytics.js       # Google Analytics
├── assets/                 # 静态资源
│   ├── images/            # 游戏缩略图
│   ├── icons/             # 分类图标
│   └── logos/             # 网站 Logo
├── .github/workflows/ci.yml # CI/CD 配置
├── .lighthouserc.json     # Lighthouse 配置
├── manifest.json          # PWA 配置
└── tasks.md              # 任务清单
```

### 核心数据结构
- **games.json**: 包含所有游戏的元数据，每个游戏必须有 id、title、iframeUrl、category 等字段
- **categories.json**: 定义游戏分类和导航结构
- **game-schema.json**: JSON Schema 用于验证数据完整性

### 页面架构
- **index.html**: 首页，包含轮播、分类导航、游戏网格
- **game.html**: 游戏详情页，使用 iframe 嵌入游戏
- **category.html**: 分类页面，支持筛选和排序
- **privacy.html**: 隐私政策页面

### JavaScript 模块
- **app.js**: 主控制器，处理页面初始化和路由
- **games.js**: 游戏数据管理，提供搜索、筛选、推荐功能
- **i18n.js**: 多语言支持 (EN/简中切换)
- **utils.js**: 通用工具函数

## 质量标准

### CI/CD 检查项
1. **数据验证**: JSON Schema 校验必须 100% 通过
2. **性能测试**: Lighthouse 各项指标 ≥ 80 分
3. **安全扫描**: 无敏感信息泄露，iframe 安全配置
4. **HTML 验证**: 所有页面通过标准验证

### SEO 要求
- 每个游戏页面独特的 meta 标签
- 自动生成 sitemap.xml
- 结构化数据标记
- Open Graph 和 Twitter 卡片

### 性能要求
- 首屏加载时间 < 3 秒
- 图片懒加载实现
- CSS/JS 文件压缩
- PWA 支持

## 进度记录

每完成一个任务必须在 `progress_log.md` 中记录：
```markdown
## YYYY-MM-DD HH:MM
- 完成任务 #编号：标题
- 时长：X min
- 结果：CI ✅/❌
- 关键改动：具体文件列表
```

## 澄清机制

遇到需求不明确时，必须在对应任务下注释 `Clarify: [具体问题]` 并暂停执行，等待项目规划者确认。

## 特殊注意事项

1. **单文件限制**: 任何单个文件不得超过 500 行，需要模块化拆分
2. **License 合规**: 不得引用非开源 License 的代码
3. **安全要求**: 禁止硬编码任何 Token 或密钥
4. **AdSense 准备**: 内容必须原创且符合 AdSense 政策要求