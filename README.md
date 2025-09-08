# Hisab - Desktop Calculator Application

A simple Excel-like desktop calculator application with spreadsheet functionality.

## 🚀 Quick Start

### 1. Download & Run (Easiest Method)
```bash
# Linux/macOS - Make executable and run
chmod +x run_hisab.sh
./run_hisab.sh

# Windows - Double-click or run in Command Prompt
run_hisab.bat

# Or run directly with Python (all platforms)
python3 hisab_app.py
```

### 2. Auto-Setup Desktop Integration (Recommended)
```bash
# Run the automated setup script
python3 setup_desktop.py
```
This will automatically create desktop shortcuts and add Hisab to your applications menu.

### 3. Manual Desktop Setup (Optional)
See the [Desktop Integration](#desktop-integration) section below for platform-specific manual instructions.

### 4. Start Using
- Click any cell and enter numbers
- Use the operation field to enter formulas like `A*B` 
- Right-click on row/column headers for quick operations

## Features

### Excel-like Interface
- Grid layout with rows (1, 2, 3...) and columns (A, B, C...)
- Editable cells for entering numeric values
- Scrollable interface for large datasets

### Formula Operations
- Operation field at the top for entering formulas
- Support for basic arithmetic: `+`, `-`, `*`, `/`
- Example: Enter `C*D` to multiply column C by column D
- Results appear in the next available column
- Formula operates on all rows: C1*D1, C2*D2, C3*D3, etc.

### Right-Click Context Menus
- **Column Operations**: Right-click on column headers (A, B, C...)
  - Sum Column: Calculate sum of all values in the column
  - Multiply/Add/Subtract/Divide: Apply operation to all cells in column
  - Clear Column: Remove all values from the column

- **Row Operations**: Right-click on row headers (1, 2, 3...)
  - Sum Row: Calculate sum of all values in the row
  - Multiply/Add/Subtract/Divide: Apply operation to all cells in row
  - Clear Row: Remove all values from the row

## Installation

### Prerequisites
- Python 3.6 or higher
- tkinter (usually included with Python)

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-tk
```

### Linux (CentOS/RHEL)
```bash
sudo yum install python3 tkinter
```

### macOS
```bash
# tkinter is included with Python from python.org
# If using Homebrew:
brew install python-tk
```

### Windows
tkinter is included with the standard Python installation from python.org

## 🖥️ Desktop Integration

### Automated Setup (Recommended)
The easiest way to set up desktop integration is to use the automated setup script:
```bash
python3 setup_desktop.py
```
This script will:
- Create desktop shortcuts (Linux)
- Add the application to your system's applications menu
- Set proper permissions on launcher scripts
- Provide platform-specific instructions for Windows and macOS

### Manual Setup Instructions

If you prefer to set up desktop integration manually, follow the platform-specific instructions below.

### Creating Desktop Shortcuts

#### Windows
1. **Using the Batch File:**
   - Right-click on `run_hisab.bat`
   - Select "Send to" → "Desktop (create shortcut)"
   - Rename the shortcut to "Hisab Calculator"

2. **Creating a Python Shortcut:**
   - Right-click on desktop → "New" → "Shortcut"
   - Enter path: `python "C:\path\to\Hisab-\hisab_app.py"`
   - Click "Next" and name it "Hisab Calculator"
   - Right-click the shortcut → "Properties" → Change icon if desired

#### Linux (Ubuntu/Debian/GNOME)
1. **Create a .desktop file:**
   ```bash
   # Create desktop entry
   cat > ~/.local/share/applications/hisab.desktop << EOF
   [Desktop Entry]
   Version=1.0
   Type=Application
   Name=Hisab Calculator
   Comment=Excel-like desktop calculator with spreadsheet functionality
   Exec=/path/to/Hisab-/run_hisab.sh
   Icon=calc
   Terminal=false
   Categories=Office;Calculator;
   EOF
   
   # Make it executable
   chmod +x ~/.local/share/applications/hisab.desktop
   ```

2. **Copy to Desktop (optional):**
   ```bash
   cp ~/.local/share/applications/hisab.desktop ~/Desktop/
   chmod +x ~/Desktop/hisab.desktop
   ```

#### macOS
1. **Using Automator (Recommended):**
   - Open Automator
   - Choose "Application"
   - Add "Run Shell Script" action
   - Enter: `/path/to/Hisab-/run_hisab.sh`
   - Save as "Hisab Calculator.app" in Applications folder

2. **Create Desktop Alias:**
   - Drag the app from Applications to Desktop while holding ⌥ (Option) + ⌘ (Command)

### Adding to System Applications Menu

#### Linux
The .desktop file method above automatically adds Hisab to your applications menu under "Office" category.

#### Windows
Create a shortcut in the Start Menu:
```batch
# Copy the shortcut to Start Menu
copy "Hisab Calculator.lnk" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\"
```

#### macOS
Copy the .app file to the Applications folder to make it available in Launchpad.

## Usage

### Starting the Application
```bash
# Make the launcher executable (Linux/macOS)
chmod +x run_hisab.sh
./run_hisab.sh

# Or run directly with Python
python3 hisab_app.py
```

### Basic Operations

1. **Enter Data**: Click on any cell and type a number
2. **Formula Operations**: 
   - Type a formula in the operation field (e.g., `A*B`, `C+D`)
   - Press Enter or click Execute
   - Results appear in the next column
3. **Right-Click Operations**:
   - Right-click column headers for column-wide operations
   - Right-click row headers for row-wide operations
4. **Clear Data**: Use "Clear All" button or right-click menu options

### Example Workflow

1. Enter values in column A: `1, 2, 3, 4`
2. Enter values in column B: `5, 6, 7, 8`
3. Type `A*B` in the operation field and press Enter
4. Results appear in column C: `5, 12, 21, 32`
5. Right-click on column C header and select "Sum Column" to get total

## 🔧 Troubleshooting

### Common Issues and Solutions

#### "Python 3 is not installed" Error
- **Windows:** Download and install Python from [python.org](https://python.org). Make sure to check "Add Python to PATH" during installation.
- **Linux:** `sudo apt install python3` (Ubuntu/Debian) or `sudo yum install python3` (CentOS/RHEL)
- **macOS:** Install from [python.org](https://python.org) or use Homebrew: `brew install python3`

#### "tkinter is not available" Error
- **Linux:** `sudo apt install python3-tk` (Ubuntu/Debian) or `sudo yum install tkinter` (CentOS/RHEL)
- **Windows/macOS:** tkinter should be included with Python. If missing, reinstall Python from [python.org](https://python.org)

#### "Permission denied" Error (Linux/macOS)
Make the script executable:
```bash
chmod +x run_hisab.sh
```

#### Application Window Doesn't Appear
1. Check if Python and tkinter are properly installed
2. Try running directly: `python3 hisab_app.py`
3. Check for error messages in the terminal
4. Ensure you're not running over SSH without X11 forwarding

#### Desktop Shortcut Doesn't Work
1. Verify the path in the shortcut is correct
2. Make sure Python is in your system PATH
3. Try running the batch/shell script directly first
4. On Linux, ensure the .desktop file has execute permissions

#### Application Runs But Crashes
1. Check Python version: `python3 --version` (requires 3.6+)
2. Look for error messages in the terminal
3. Try running the test file: `python3 test_hisab.py`

### Getting Help
If you encounter issues not covered here:
1. Check the terminal/command prompt for error messages
2. Verify your Python installation: `python3 -c "import tkinter; print('OK')"`
3. Open an issue on the GitHub repository with:
   - Your operating system and version
   - Python version (`python3 --version`)
   - Complete error message
   - Steps you tried to fix it

## Files

- `hisab_app.py` - Main application file
- `run_hisab.sh` - Launcher script (Linux/macOS)
- `run_hisab.bat` - Launcher script (Windows)
- `setup_desktop.py` - Automated desktop integration setup
- `requirements.txt` - Documentation of requirements
- `test_hisab.py` - Test suite for core functionality
- `demo.py` - Feature demonstration script
- `README.md` - This documentation

## License

Open source - feel free to modify and distribute.