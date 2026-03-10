@echo on
chcp 65001 >nul
setlocal enabledelayedexpansion

rem === Define base paths ===
set "BASE_TOOLS_PATH=%~dp0"
set "NODE_PATH=%BASE_TOOLS_PATH%node-v22.21.1-win-x64"
set "PYTHON_PATH=%BASE_TOOLS_PATH%Python312"
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_NAME=OpenClaw.lnk"
set "TARGET_BAT=%BASE_TOOLS_PATH%start_tray.bat"

rem === Check and add Node.js path ===
echo !PATH! | findstr /C:"%NODE_PATH%" >nul
if errorlevel 1 set "PATH=%NODE_PATH%;!PATH!"

rem === Check and add Python path ===
echo !PATH! | findstr /C:"%PYTHON_PATH%" >nul
if errorlevel 1 set "PATH=%PYTHON_PATH%;!PATH!"

rem === Check if target file exists ===
if not exist "%TARGET_BAT%" (
    echo Target file not found: %TARGET_BAT%
    pause
    exit /b 1
)

echo OpenClaw System Tray Application - Startup Installation Tool
echo.
echo Target path: %TARGET_BAT%
echo Startup folder: %STARTUP_FOLDER%
echo.

rem === Check if shortcut already exists ===
set "SHORTCUT_PATH=%STARTUP_FOLDER%\%SHORTCUT_NAME%"
if exist "%SHORTCUT_PATH%" (
    echo Existing shortcut detected
    echo.
    choice /C YN /M "Overwrite existing startup item? (Y=Yes, N=No)"
    if errorlevel 2 (
        echo Installation cancelled
        pause
        exit /b 0
    )
    del "%SHORTCUT_PATH%"
)

rem === Create shortcut ===
echo Creating shortcut...

set "VBS_SCRIPT=%TEMP%\create_shortcut.vbs"
(
echo Set shell = CreateObject^("WScript.Shell"^)
echo Set shortcut = shell.CreateShortcut^("%SHORTCUT_PATH%"^)
echo shortcut.TargetPath = "%TARGET_BAT%"
echo shortcut.WorkingDirectory = "%BASE_TOOLS_PATH%"
echo shortcut.Description = "OpenClaw System Tray Application"
echo shortcut.Save
) > "%VBS_SCRIPT%"

cscript //NoLogo "%VBS_SCRIPT%"
del "%VBS_SCRIPT%"

if exist "%SHORTCUT_PATH%" (
    echo Shortcut created successfully!
    echo.
    echo Shortcut path: %SHORTCUT_PATH%
    echo.
    echo OpenClaw System Tray Application has been added to startup
    echo It will automatically run when Windows starts
    echo.
    choice /C YN /M "Start tray application now? (Y=Yes, N=No)"
    if not errorlevel 2 (
        echo Starting tray application...
        start "" "%TARGET_BAT%"
    )
) else (
    echo Failed to create shortcut!
)

echo.
pause