@echo off
echo =====================================
echo GitHub推送重试脚本
echo =====================================

:retry
echo.
echo 尝试拉取远程更新...
git pull origin main --rebase
if %ERRORLEVEL% NEQ 0 (
    echo 拉取失败，等待5秒后重试...
    timeout /t 5 >nul
    goto retry
)

echo.
echo 尝试推送到GitHub...
git push origin main
if %ERRORLEVEL% NEQ 0 (
    echo 推送失败，等待5秒后重试...
    timeout /t 5 >nul
    goto retry
)

echo.
echo =====================================
echo 成功推送到GitHub！
echo =====================================
echo.
echo 现在可以：
echo 1. 检查GitHub仓库确认文件已上传
echo 2. 进入Actions查看工作流运行状态
echo 3. 等待Cloudflare Pages自动部署
echo.
pause