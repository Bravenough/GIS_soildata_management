@echo off
echo 正在启动前端服务...
echo.
echo 请选择启动方式：
echo 1. 使用HBuilderX（推荐）
echo 2. 使用测试页面
echo 3. 尝试安装uni-app CLI
echo.
set /p choice=请输入选择 (1-3): 

if "%choice%"=="1" (
    echo.
    echo 请按以下步骤操作：
    echo 1. 打开 HBuilderX
    echo 2. 点击"文件" → "打开目录"
    echo 3. 选择当前项目文件夹
    echo 4. 右键项目根目录，选择"运行" → "运行到浏览器" → "Chrome"
    pause
) else if "%choice%"=="2" (
    echo 正在打开API测试页面...
    start http://localhost:8080/test.html
) else if "%choice%"=="3" (
    echo 正在安装 uni-app CLI...
    npm install -g @dcloudio/cli
    echo 安装完成，请重新运行项目
    pause
) else (
    echo 无效选择，请重新运行脚本
    pause
) 