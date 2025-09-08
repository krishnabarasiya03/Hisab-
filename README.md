# Hisab - Desktop Calculator Application

A modern Excel-like desktop calculator application with spreadsheet functionality, built with **JavaScript, React, and Electron**.

## 🚀 Quick Start

### JavaScript/React/Electron Version (Recommended)

```bash
# Prerequisites: Node.js 16+ and npm
# Install from https://nodejs.org/

# 1. Install dependencies
npm install

# 2. Build the React app
npm run build

# 3. Start the Electron application
npm start

# OR use the launcher scripts:
# Linux/macOS
chmod +x run_hisab.sh
./run_hisab.sh

# Windows
run_hisab.bat
```

### Development Mode
```bash
# Start React dev server + Electron with hot reloading
npm run dev

# Or start just the React dev server
npm run dev-react
```

### Create Distribution Packages
```bash
# Create platform-specific installers (.exe, .dmg, .AppImage)
npm run dist
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

## Technology Stack

**Modern JavaScript/React/Electron Implementation**:
- **Frontend**: React.js with modern hooks and components
- **Desktop**: Electron.js for cross-platform native applications
- **Build System**: webpack (via create-react-app) and npm scripts
- **Packaging**: electron-builder for creating installers
- **Styling**: Modern CSS with responsive design

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

### JavaScript/React/Electron Version (Recommended)

#### Prerequisites
- Node.js 16 or higher
- npm (comes with Node.js)

#### Download Node.js
- **All Platforms**: [nodejs.org](https://nodejs.org/) - Download LTS version
- **Windows**: Download installer and check "Add to PATH"
- **macOS**: `brew install node` or download from nodejs.org
- **Linux**: 
  ```bash
  # Ubuntu/Debian
  curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
  sudo apt-get install -y nodejs
  
  # CentOS/RHEL
  curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
  sudo yum install -y nodejs
  ```

#### Install and Run
```bash
# Clone or download the repository
git clone https://github.com/krishnabarasiya03/Hisab-.git
cd Hisab-

# Install dependencies
npm install

# Build the React application
npm run build

# Start the Electron app
npm start
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install nodejs npm
```

### Linux (CentOS/RHEL)
```bash
sudo yum install nodejs npm
```

### macOS
```bash
# Using Homebrew:
brew install node

# Or download from nodejs.org
```

### Windows
Download and install Node.js from [nodejs.org](https://nodejs.org), making sure to check "Add to PATH" option.

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

#### JavaScript/React/Electron Version
```bash
# Production mode
npm start

# Development mode (with hot reloading)
npm run dev

# Using launcher scripts
./run_hisab.sh        # Linux/macOS
run_hisab.bat         # Windows
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

#### JavaScript/React/Electron Version

##### "Node.js is not installed" Error
- **All Platforms:** Download and install Node.js from [nodejs.org](https://nodejs.org). Choose the LTS version.
- **Windows:** Make sure to check "Add to PATH" during installation
- **Linux:** Use your package manager or NodeSource repository
- **macOS:** Install from nodejs.org or use Homebrew: `brew install node`

##### "npm command not found" Error
- npm comes with Node.js. If it's missing, reinstall Node.js
- On Linux, you might need to install npm separately: `sudo apt install npm`

##### Application Doesn't Start
1. Make sure all dependencies are installed: `npm install`
2. Build the React app: `npm run build`
3. Check for error messages in the terminal
4. Try development mode: `npm run dev`

##### Build Fails
1. Clear npm cache: `npm cache clean --force`
2. Delete node_modules and reinstall: `rm -rf node_modules && npm install`
3. Make sure you have enough disk space
4. Check Node.js version: `node --version` (should be 16+)

##### Electron App Shows Blank Screen
1. Make sure React app is built: `npm run build`
2. Check browser console for errors (Ctrl+Shift+I)
3. Try starting with development mode: `npm run dev`

#### "Permission denied" Error (Linux/macOS)
Make the script executable:
```bash
chmod +x run_hisab.sh
```

### Getting Help
If you encounter issues not covered here:

1. Check the terminal/command prompt for error messages
2. Verify your Node.js installation: `node --version && npm --version`
3. Try clearing cache and reinstalling: `npm cache clean --force && rm -rf node_modules && npm install`
4. Open an issue on the GitHub repository with:
   - Your operating system and version
   - Your operating system and version
   - Node.js version (`node --version`)
   - npm version (`npm --version`)
   - Complete error message
   - Steps you tried to fix it

## Files

- `package.json` - npm project configuration and dependencies
- `main.js` - Electron main process (desktop app)
- `src/App.js` - Main React application component
- `src/components/` - React UI components (SpreadsheetGrid, OperationBar, ContextMenu)
- `src/utils/` - Business logic (calculator.js, operations.js)
- `public/index.html` - HTML template for React app
- `src/App.css` - Modern styling and responsive design
- `run_hisab.sh` - Launcher script (Linux/macOS)
- `run_hisab.bat` - Launcher script (Windows)
- `test_hisab.js` - Core functionality tests for Node.js
- `demo.js` - Feature demonstration script
- `setup_desktop.py` - Automated desktop integration setup
- `README.md` - This documentation

## License

Open source - feel free to modify and distribute.