# GitHub 同步和配置指导

## 第一步：推送代码到GitHub仓库

### 1.1 检查当前Git状态
```bash
git status
git log --oneline -5
```

### 1.2 添加所有新文件和修改
```bash
# 添加所有新文件
git add .

# 检查待提交的文件
git status

# 提交更改
git commit -m "feat: 实现游戏库扩充和自动化监控系统

- 添加5款新游戏 (Car Racing 3D, Soccer Physics, Stick War Legacy, Fruit Ninja HTML5, Tower Defense HTML5)
- 实现GitHub Actions每周自动健康检查
- 添加游戏发现和验证系统
- 为所有游戏添加版权合规字段 (license, commercial_use, ad_allowed)
- 创建失败游戏自动下线机制
- 新增本地验证脚本确保代码质量

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 1.3 推送到GitHub
```bash
# 推送到主分支
git push origin main

# 如果推送失败，先拉取远程更新
git pull origin main --rebase
git push origin main
```

## 第二步：配置GitHub Actions权限

### 2.1 启用GitHub Actions
1. 进入你的GitHub仓库页面
2. 点击顶部的 **"Actions"** 标签
3. 如果Actions被禁用，点击 **"I understand my workflows, go ahead and enable them"**

### 2.2 配置工作流权限
1. 在仓库页面，点击 **"Settings"**
2. 在左侧菜单找到 **"Actions"** → **"General"**
3. 滚动到 **"Workflow permissions"** 部分
4. 选择 **"Read and write permissions"**
5. 勾选 **"Allow GitHub Actions to create and approve pull requests"**
6. 点击 **"Save"** 保存设置

### 2.3 验证工作流文件
确保以下文件存在并正确配置：
- `.github/workflows/weekly-health-check.yml`

## 第三步：配置Cloudflare Pages部署

### 3.1 连接GitHub仓库
1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 进入 **"Pages"** 部分
3. 点击 **"Create a project"**
4. 选择 **"Connect to Git"**
5. 授权访问你的GitHub账户
6. 选择你的游戏网站仓库

### 3.2 配置构建设置
- **Production branch**: `main`
- **Build command**: (留空)
- **Build output directory**: `/`
- **Root directory**: `/`

### 3.3 环境变量设置
如果需要环境变量，可以在 **"Settings"** → **"Environment variables"** 中添加

### 3.4 自定义域名 (可选)
1. 在 **"Custom domains"** 中添加你的域名 `usgamehub.icu`
2. 按照提示配置DNS记录

## 第四步：测试自动化系统

### 4.1 手动触发工作流
1. 进入GitHub仓库的 **"Actions"** 页面
2. 点击左侧的 **"Weekly Health Check"**
3. 点击 **"Run workflow"** 按钮
4. 选择分支为 `main`，点击 **"Run workflow"**

### 4.2 监控工作流执行
1. 观察工作流的执行状态
2. 检查日志输出是否正常
3. 确认是否有自动提交生成

### 4.3 验证定时任务
- 工作流配置为每周一3点UTC自动运行
- 首次部署后等待一周验证自动运行

## 第五步：验证网站功能

### 5.1 访问部署的网站
- Cloudflare Pages会提供一个 `.pages.dev` 的预览链接
- 使用自定义域名 `usgamehub.icu` (如果已配置)

### 5.2 功能测试清单
- [ ] 首页加载正常，显示14款游戏
- [ ] 游戏页面iframe嵌入正常工作
- [ ] Google Analytics追踪代码正常工作 (检查GA面板)
- [ ] 新窗口模式对不兼容游戏正常工作
- [ ] 移动设备响应式布局正常

## 第六步：监控和维护

### 6.1 设置GitHub通知
1. 在仓库页面，点击 **"Watch"** → **"Custom"**
2. 勾选 **"Actions"** 接收工作流通知
3. 配置邮件通知偏好

### 6.2 定期检查
- **每周查看**: Actions执行结果
- **每月检查**: 游戏可用性报告
- **按需更新**: 发现问题游戏时查看 `data/inactive_games.json`

### 6.3 扩展新游戏
使用游戏发现脚本添加新游戏：
```bash
python scripts/game_discovery.py
python scripts/integrate_new_games.py
```

## 故障排除

### 常见问题及解决方案

#### 工作流权限错误
```
Error: Permission denied to github-actions[bot]
```
**解决方案**: 检查第二步中的权限配置

#### 推送失败
```
! [rejected] main -> main (fetch first)
```
**解决方案**: 
```bash
git pull origin main --rebase
git push origin main
```

#### 游戏加载失败
**解决方案**: 运行健康检查脚本
```bash
python scripts/check_games.py
```

#### JSON Schema验证失败
**解决方案**: 运行本地验证
```bash
python scripts/local_validation.py
```

## 成功指标

系统成功部署后，你应该看到：
- ✅ GitHub Actions每周自动运行
- ✅ 游戏健康状况自动监控
- ✅ 故障游戏自动下线
- ✅ 网站在Cloudflare Pages正常运行
- ✅ Google Analytics数据正常收集
- ✅ 14款游戏全部可正常游玩

## 联系支持

如果遇到技术问题：
1. 检查GitHub Actions日志
2. 运行 `python scripts/local_validation.py` 诊断
3. 查看Cloudflare Pages部署日志