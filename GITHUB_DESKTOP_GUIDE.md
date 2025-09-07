# GitHub Desktop 中文使用指南

## 第一步：设置中文语言

### 方法1：修改语言设置
1. 打开GitHub Desktop
2. 点击左上角菜单 **"File"** → **"Options"**
3. 在Settings页面，找到 **"Language"** 下拉菜单
4. 选择 **"简体中文"** 或 **"Chinese (Simplified)"**
5. 点击 **"Save"** 保存
6. 重启GitHub Desktop应用

### 方法2：如果没有中文选项
GitHub Desktop最新版本可能暂时不支持中文，但操作很简单，我会用中英文对照教你。

## 第二步：登录GitHub账户

1. 启动GitHub Desktop
2. 点击 **"Sign in to GitHub.com"** (登录到GitHub.com)
3. 输入你的GitHub用户名和登录凭证
4. 完成两步验证（如果开启了的话）

## 第三步：克隆你的仓库

### 方式1：从GitHub.com克隆
1. 点击主界面的 **"Clone a repository from the Internet"**
   中文翻译：从互联网克隆仓库
2. 在URL标签页，输入：`https://github.com/ZZZ01975/usgamehub.icu.git`
3. 选择本地保存位置（建议创建新文件夹）
4. 点击 **"Clone"** (克隆)

### 方式2：添加现有本地仓库
1. 点击 **"Add an Existing Repository"** 
   中文翻译：添加现有仓库
2. 选择你的项目文件夹：`C:\Users\israe\Desktop\games-0905`
3. 点击 **"Add Repository"** (添加仓库)

## 第四步：日常使用操作

### 🔄 同步更新 (最常用)
- **"Fetch origin"** = 获取远程更新
- **"Pull origin"** = 拉取并合并更新  
- **"Push origin"** = 推送本地更改

### 📝 提交更改
1. 左侧会显示所有更改的文件
2. 在底部输入框写提交信息（中文即可）
3. 点击 **"Commit to main"** (提交到主分支)
4. 点击 **"Push origin"** (推送到远程)

### 📁 查看更改
- **"Changes"** = 更改列表
- **"History"** = 提交历史
- **"Repository"** = 仓库设置

## 第五步：常用按钮中英文对照

| 英文 | 中文含义 | 用途 |
|------|----------|------|
| **Repository** | 仓库 | 仓库设置和操作 |
| **File** | 文件 | 文件菜单 |
| **Edit** | 编辑 | 编辑菜单 |
| **View** | 查看 | 视图设置 |
| **Repository > Clone** | 克隆仓库 | 下载远程仓库到本地 |
| **Fetch origin** | 获取远程 | 检查远程是否有更新 |
| **Pull origin** | 拉取远程 | 下载远程更新到本地 |
| **Push origin** | 推送远程 | 上传本地更改到远程 |
| **Commit to main** | 提交到主分支 | 保存更改到本地Git |
| **Sync** | 同步 | 自动拉取和推送 |
| **Changes** | 更改 | 显示修改的文件 |
| **History** | 历史 | 显示提交记录 |
| **Summary** | 摘要 | 提交信息标题 |
| **Description** | 描述 | 提交信息详细说明 |
| **Undo** | 撤销 | 撤销上次操作 |

## 第六步：完整工作流程

### 📥 每次开始工作前：
1. 打开GitHub Desktop
2. 点击 **"Fetch origin"** (检查更新)
3. 如果有更新，点击 **"Pull origin"** (拉取更新)

### 💾 完成修改后：
1. 查看 **"Changes"** 标签页的文件列表
2. 在 **"Summary"** 框输入更改说明（如：修复游戏Bug）
3. 点击 **"Commit to main"** (提交)
4. 点击 **"Push origin"** (推送到GitHub)

### 🔄 自动同步：
- 点击右上角的 **"Sync"** 按钮可以自动拉取+推送

## 第七步：解决常见问题

### 问题1：推送失败
**显示**: "Push rejected" 或 "conflict"
**解决**: 
1. 先点击 **"Pull origin"**
2. 如果有冲突，GitHub Desktop会帮你标记
3. 解决冲突后重新提交

### 问题2：找不到仓库
**解决**:
1. 确认GitHub用户名和登录凭证正确
2. 确认仓库URL: `https://github.com/ZZZ01975/usgamehub.icu.git`
3. 检查网络连接

### 问题3：文件太多
**解决**:
- 可以在 **"Changes"** 中选择性提交文件
- 右键点击文件选择 **"Discard changes"** 忽略不需要的更改

## 第八步：高级功能

### 🌿 分支管理
- **"Current branch: main"** = 当前分支：主分支
- **"New branch"** = 创建新分支
- **"Switch branch"** = 切换分支

### 📋 提交历史
- 点击 **"History"** 查看所有提交记录
- 点击某个提交查看具体更改
- 右键点击提交可以撤销或创建标签

### ⚙️ 设置选项
- **File > Options > Git** = Git用户信息设置
- **File > Options > Advanced** = 高级设置
- **Repository > Repository Settings** = 当前仓库设置

## 快速操作卡片

```
🚀 日常三步走：
1. Fetch origin (检查更新)
2. 修改文件
3. Commit + Push (提交推送)

🔧 出现问题：
1. Pull origin (拉取解决)
2. 解决冲突
3. 重新 Commit + Push

📱 一键同步：
点击右上角 "Sync" 按钮
```

## 给你的专用操作步骤

既然你的仓库已经推送成功，现在用GitHub Desktop的步骤：

### 首次设置：
1. 打开GitHub Desktop
2. **File** → **Options** → 查看是否有中文选项
3. **Clone a repository** → 输入：`https://github.com/ZZZ01975/usgamehub.icu.git`
4. 选择保存位置（建议新建文件夹）

### 以后每次修改：
1. 在Windows文件管理器中修改项目文件
2. 打开GitHub Desktop，会自动显示更改
3. 写提交信息（中文即可）
4. 点击 **"Commit to main"**
5. 点击 **"Push origin"**

这样就不用记复杂的Git命令了！

## 联系我获取帮助

如果遇到任何问题：
1. 截图发给我你看到的英文界面
2. 告诉我你想做什么操作
3. 我会给你准确的中英文对照指导