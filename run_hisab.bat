@echo off
REM Hisab Calculator - Windows Launcher Script
REM Builds and runs the Electron application

echo 🧮 Starting Hisab Calculator...

REM Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if npm is installed
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ npm is not installed. Please install npm
    pause
    exit /b 1
)

echo 📦 Checking dependencies...

REM Check if node_modules exists
if not exist "node_modules" (
    echo 📥 Installing dependencies...
    call npm install
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

echo 🔨 Building React app...
call npm run build
if %errorlevel% neq 0 (
    echo ❌ Failed to build React app
    pause
    exit /b 1
)

echo 🚀 Starting Hisab Calculator...
call npm start

echo ✅ Hisab Calculator closed successfully
pause