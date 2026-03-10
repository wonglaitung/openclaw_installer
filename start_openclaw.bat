@echo on
chcp 65001 >nul
setlocal enabledelayedexpansion

rem === 定义基础路径 ===
set "BASE_TOOLS_PATH=%~dp0"
set "NODE_PATH=%BASE_TOOLS_PATH%node-v22.21.1-win-x64"
set "PYTHON_PATH=%BASE_TOOLS_PATH%Python312"

rem === 定义网页地址 ===
set "WEB_URL=http://localhost:18789/#token=c1956e2f9bd62dfac41f31b0ebf22586f720913d495d3c6e"

rem === 检查并添加路径 ===
echo !PATH! | findstr /C:"%NODE_PATH%" >nul
if errorlevel 1 set "PATH=%NODE_PATH%;!PATH!"

echo !PATH! | findstr /C:"%PYTHON_PATH%" >nul
if errorlevel 1 set "PATH=%PYTHON_PATH%;!PATH!"

rem === 根据参数执行命令 ===
echo.

if "%1"=="" (
    rem 情况一：无参数 → gateway + 打开网页
    echo [→] 打开网页：%WEB_URL%
    start "" "%WEB_URL%"
    echo [→] 执行：openclaw gateway
    call openclaw gateway
) else if /i "%1"=="onboard" (
    rem 情况二：onboard → 不打开网页
    echo [→] 执行：openclaw onboard
    call openclaw onboard
) else if /i "%1"=="gateway" (
    rem 情况三：gateway → 打开网页
    echo [→] 打开网页：%WEB_URL%
    start "" "%WEB_URL%"
    echo [→] 执行：openclaw gateway
    call openclaw gateway
)