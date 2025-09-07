# GitHub 手动上传指南

如果命令行方式遇到问题，可以使用GitHub网页界面手动上传所有文件。

## 方案一：使用命令行脚本（推荐）

1. **双击运行**: `git_upload_commands.bat`
2. **按提示操作**: 脚本会暂停让你确认每一步
3. **等待完成**: 自动处理所有Git操作

## 方案二：手动上传（备用方案）

### 步骤1：准备上传文件夹
创建一个新文件夹，复制以下文件和文件夹到其中：

#### 必须上传的文件夹:
```
📁 .github/workflows/     (GitHub Actions工作流)
📁 css/                   (样式文件)
📁 data/                  (游戏数据库)
📁 games/hosted/          (自建游戏) 
📁 js/                    (JavaScript文件)
📁 scripts/               (Python脚本)
```

#### 必须上传的文件:
```
📄 index.html            (首页)
📄 game.html             (游戏页面)
📄 category.html         (分类页面)
📄 privacy.html          (隐私政策)
📄 _headers              (HTTP头配置)
📄 _redirects            (路由配置)
📄 manifest.json         (PWA配置)
📄 robots.txt            (搜索引擎规则)
📄 progress_log.md       (进度日志)
📄 GITHUB_SETUP_GUIDE.md (部署指导)
📄 DEPLOYMENT_READY.md   (部署文档)
📄 ANALYTICS_INTEGRATION_SUMMARY.md (分析集成文档)
```

### 步骤2：删除不需要的文件
**删除这些文件**（不要上传）:
```
❌ git_upload_commands.bat
❌ MANUAL_UPLOAD_GUIDE.md  
❌ scripts/local_validation.py (可选，本地验证用)
❌ scripts/clean_schema_conflicts.py (临时脚本)
❌ data/games_backup_*.json (备份文件)
```

### 步骤3：GitHub网页上传

1. **登录GitHub**: 进入你的仓库页面
2. **点击"Add file"** → **"Upload files"**
3. **拖拽文件夹**: 将准备好的文件夹拖到上传区域
4. **等待上传**: GitHub会自动处理文件夹结构
5. **填写提交信息**:
   ```
   Title: feat: 实现游戏库扩充和自动化监控系统
   
   Description:
   - 添加5款新游戏，总数从9款扩充至14款 (+55.6%增长)  
   - 实现GitHub Actions每周自动健康检查和故障游戏自动下线
   - 创建游戏发现验证系统，新游戏验证成功率71.4%
   - 为所有游戏添加版权合规字段支持AdSense审核
   - 新增本地验证工具和完整GitHub部署指导文档
   
   🤖 Generated with Claude Code
   Co-Authored-By: Claude <noreply@anthropic.com>
   ```
6. **点击"Commit changes"**

### 步骤4：验证上传结果

上传完成后，检查仓库是否包含以下结构：
```
your-repo/
├── .github/workflows/weekly-health-check.yml ✅
├── css/ ✅
├── data/games.json ✅ (14个游戏)
├── games/hosted/ ✅
├── js/ ✅  
├── scripts/ ✅ (Python脚本)
├── index.html ✅
├── game.html ✅
└── 其他核心文件 ✅
```

## 验证成功标志

### GitHub Actions激活
1. 进入仓库的 **"Actions"** 标签页
2. 应该看到 **"Weekly Health Check"** 工作流
3. 状态显示为绿色或待运行

### Cloudflare Pages自动部署  
1. Cloudflare Pages会自动检测到推送
2. 开始新的部署过程
3. 几分钟后网站会更新

### 网站功能验证
访问你的网站 https://usgamehub.icu/ 确认：
- ✅ 显示14个游戏（比之前多5个）
- ✅ 新游戏可以正常加载
- ✅ Google Analytics正常工作

## 如果遇到问题

### 上传失败
- 检查文件大小（GitHub单文件限制100MB）
- 分批上传，先上传小文件再上传大文件夹

### Actions不工作
- 进入 Settings → Actions → General
- 确保选择了 "Allow all actions and reusable workflows"
- 设置 Workflow permissions 为 "Read and write permissions"

### 部署不更新
- 检查Cloudflare Pages部署日志
- 确认推送的分支是main
- 手动触发Cloudflare Pages重新部署

## 支持联系

如果两种方式都遇到问题：
1. 截图错误信息
2. 运行 `python scripts/local_validation.py` 检查本地状态
3. 检查网络连接和GitHub访问