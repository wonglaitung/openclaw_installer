@echo on
chcp 65001 >nul
setlocal enabledelayedexpansion

rem === Define base paths ===
set "BASE_TOOLS_PATH=%~dp0"
set "NODE_PATH=%BASE_TOOLS_PATH%node-v22.21.1-win-x64"
set "PYTHON_PATH=%BASE_TOOLS_PATH%Python312"

rem === Check and add Node.js path ===
echo !PATH! | findstr /C:"%NODE_PATH%" >nul
if errorlevel 1 set "PATH=%NODE_PATH%;!PATH!"

rem === Check and add Python path ===
echo !PATH! | findstr /C:"%PYTHON_PATH%" >nul
if errorlevel 1 set "PATH=%PYTHON_PATH%;!PATH!"

rem === Check if pystray and Pillow are installed ===
echo Checking dependencies...
"%PYTHON_PATH%\python.exe" -c "import pystray, PIL" >nul 2>&1
if errorlevel 1 (
    echo Dependencies not found, installing...
    "%PYTHON_PATH%\Scripts\pip3.exe" install pystray Pillow
    if errorlevel 1 (
        echo Failed to install dependencies!
        pause
        exit /b 1
    )
    echo Dependencies installed successfully!
) else (
    echo Dependencies already installed
)

rem === Start tray application ===
echo.
echo Starting OpenClaw System Tray Application...
echo.

cd /d "%BASE_TOOLS_PATH%"
start "" /B "%PYTHON_PATH%\pythonw.exe" tray_app.py