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

rem === Check and initialize user .openclaw directory ===
set "USER_OPENCLAW=%USERPROFILE%\.openclaw"
set "PROJECT_OPENCLAW=%BASE_TOOLS_PATH%.openclaw"
set "CONFIG_FILE=%USER_OPENCLAW%\openclaw.json"
set "WORKSPACE_PATH=%USER_OPENCLAW%\workspace"
set "TEMP_PY_SCRIPT=%TEMP%\update_workspace.py"

if not exist "%USER_OPENCLAW%" (
    echo User .openclaw directory not found, initializing from project...
    echo Creating directory: %USER_OPENCLAW%
    xcopy "%PROJECT_OPENCLAW%" "%USER_OPENCLAW%\" /E /I /Y /Q
    if errorlevel 1 (
        echo Failed to copy initial configuration!
        pause
        exit /b 1
    )

    rem === Update workspace path in configuration ===
    echo Updating workspace path in configuration...
    echo Workspace path: %WORKSPACE_PATH%

    rem Create a temporary Python script to update JSON
    echo import json > "%TEMP_PY_SCRIPT%"
    echo import os >> "%TEMP_PY_SCRIPT%"
    echo. >> "%TEMP_PY_SCRIPT%"
    echo config_file = r'%CONFIG_FILE%' >> "%TEMP_PY_SCRIPT%"
    echo workspace_path = r'%WORKSPACE_PATH%' >> "%TEMP_PY_SCRIPT%"
    echo. >> "%TEMP_PY_SCRIPT%"
    echo with open^(config_file, 'r', encoding='utf-8'^) as f: >> "%TEMP_PY_SCRIPT%"
    echo     config = json.load^(f^) >> "%TEMP_PY_SCRIPT%"
    echo. >> "%TEMP_PY_SCRIPT%"
    echo if 'agents' in config and 'defaults' in config['agents']: >> "%TEMP_PY_SCRIPT%"
    echo     config['agents']['defaults']['workspace'] = workspace_path >> "%TEMP_PY_SCRIPT%"
    echo     with open^(config_file, 'w', encoding='utf-8'^) as f: >> "%TEMP_PY_SCRIPT%"
    echo         json.dump^(config, f, indent=2, ensure_ascii=False^) >> "%TEMP_PY_SCRIPT%"
    echo     print^('Configuration updated successfully'^) >> "%TEMP_PY_SCRIPT%"
    echo else: >> "%TEMP_PY_SCRIPT%"
    echo     print^('Warning: workspace path not found in configuration'^) >> "%TEMP_PY_SCRIPT%"

    rem Run Python script
    "%PYTHON_PATH%\python.exe" "%TEMP_PY_SCRIPT%"

    if errorlevel 1 (
        echo Failed to update configuration file!
        del "%TEMP_PY_SCRIPT%" 2>nul
        pause
        exit /b 1
    )

    rem Clean up temporary script
    del "%TEMP_PY_SCRIPT%" 2>nul
    echo Configuration initialized successfully!
) else (
    echo User .openclaw directory already exists
)

rem === Check if OpenClaw is already running ===
echo Checking if OpenClaw is already running...
netstat -ano | findstr :18789 >nul 2>&1
if not errorlevel 1 (
    echo.
    echo ================================================
    echo ERROR: OpenClaw is already running!
    echo ================================================
    echo.
    echo Port 18789 is already in use, which means OpenClaw Gateway is already running.
    echo.
    echo Please choose one of the following options:
    echo   1. Stop the current instance before starting a new one
    echo   2. Use the existing instance
    echo.
    echo To stop the current instance:
    echo   - Right-click the OpenClaw icon in the system tray and select "Exit"
    echo   - Or run: taskkill /F /IM pythonw.exe
    echo.
    pause
    exit /b 1
)
echo OpenClaw is not running, ready to start...
echo.

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