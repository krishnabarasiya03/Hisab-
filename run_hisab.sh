#!/bin/bash
# Hisab Desktop Application Launcher

echo "Starting Hisab Desktop Application..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed!"
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

# Check if tkinter is available
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: tkinter is not available!"
    echo "Please install tkinter:"
    echo "  Ubuntu/Debian: sudo apt install python3-tk"
    echo "  CentOS/RHEL: sudo yum install tkinter"
    echo "  macOS: tkinter should be included with Python"
    echo "  Windows: tkinter should be included with Python"
    exit 1
fi

# Run the application
python3 hisab_app.py