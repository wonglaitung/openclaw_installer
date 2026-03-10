@echo on
chcp 65001 >nul
setlocal enabledelayedexpansion

rem === Define base paths ===
set "BASE_TOOLS_PATH=%~dp0"
set "NODE_PATH=%BASE_TOOLS_PATH%node-v22.21.1-win-x64"
set "PYTHON_PATH=%BASE_TOOLS_PATH%Python312"
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_NAME=OpenClaw.lnk"
set "SHORTCUT_PATH=%STARTUP_FOLDER%\%SHORTCUT_NAME%"

rem === Check and add Node.js path ===
echo !PATH! | findstr /C:"%NODE_PATH%" >nul
if errorlevel 1 set "PATH=%NODE_PATH%;!PATH!"

rem === Check and add Python path ===
echo !PATH! | findstr /C:"%PYTHON_PATH%" >nul
if errorlevel 1 set "PATH=%PYTHON_PATH%;!PATH!"

echo OpenClaw System Tray Application - Startup Uninstallation Tool
echo.

rem === Check if shortcut exists ===
if not exist "%SHORTCUT_PATH%" (
    echo Startup shortcut not found
    echo Path: %SHORTCUT_PATH%
    echo.
    pause
    exit /b 0
)

echo Startup shortcut found:
echo Path: %SHORTCUT_PATH%
echo.

rem === Confirm deletion ===
choice /C YN /M "Remove OpenClaw tray application from startup? (Y=Yes, N=No)"
if errorlevel 2 (
    echo Uninstallation cancelled
    pause
    exit /b 0
)

rem === Delete shortcut ===
echo Deleting shortcut...
del "%SHORTCUT_PATH%"

if exist "%SHORTCUT_PATH%" (
    echo Deletion failed! Please delete manually:
    echo %SHORTCUT_PATH%
) else (
    echo OpenClaw tray application has been successfully removed from startup
)

echo.
pause