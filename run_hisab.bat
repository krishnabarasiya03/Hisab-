@echo off
REM Hisab Calculator - Windows Launcher Script
REM Builds and runs the Electron application
setlocal enabledelayedexpansion

echo 🧮 Starting Hisab Calculator...

REM Check if we're in the correct directory
if not exist "package.json" (
    echo ❌ Error: package.json not found. Please run this script from the Hisab Calculator directory.
    pause
    exit /b 1
)

REM Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js from https://nodejs.org/
    echo    Make sure to download the LTS version and check "Add to PATH" during installation.
    pause
    exit /b 1
)

REM Check Node.js version
for /f "tokens=1 delims=." %%a in ('node --version') do set major_version=%%a
set major_version=%major_version:~1%
if %major_version% LSS 16 (
    echo ❌ Node.js version is too old. Please install Node.js 16 or higher.
    echo    Current version: 
    node --version
    pause
    exit /b 1
)

REM Check if npm is installed
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ npm is not installed. Please reinstall Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js and npm are installed
echo 📦 Checking dependencies...

REM Check if node_modules exists
if not exist "node_modules" (
    echo 📥 Installing dependencies... This may take a few minutes.
    call npm install
    if !errorlevel! neq 0 (
        echo ❌ Failed to install dependencies
        echo    Try running: npm cache clean --force
        echo    Then: npm install
        pause
        exit /b 1
    )
) else (
    echo ✅ Dependencies already installed
)

echo 🔨 Building React app...
call npm run build
if %errorlevel% neq 0 (
    echo ❌ Failed to build React app
    echo    Try running: npm cache clean --force
    echo    Then: npm install && npm run build
    pause
    exit /b 1
)

echo ✅ Build successful
echo 🚀 Starting Hisab Calculator...

REM Start the application with error handling
call npm start
set app_exit_code=%errorlevel%

if %app_exit_code% neq 0 (
    echo ❌ Application exited with error code: %app_exit_code%
    echo    For troubleshooting, see README.md
) else (
    echo ✅ Hisab Calculator closed successfully
)

pause