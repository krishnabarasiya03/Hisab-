#!/bin/bash

# Hisab Calculator - Linux/macOS Launcher Script
# Builds and runs the Electron application

echo "🧮 Starting Hisab Calculator..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js from https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm"
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📦 Checking dependencies..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📥 Installing dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi

echo "🔨 Building React app..."
npm run build
if [ $? -ne 0 ]; then
    echo "❌ Failed to build React app"
    exit 1
fi

echo "🚀 Starting Hisab Calculator..."
npm start

echo "✅ Hisab Calculator closed successfully"