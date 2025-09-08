# Hisab - Desktop Calculator Application

A simple Excel-like desktop calculator application with spreadsheet functionality.

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

## Files

- `hisab_app.py` - Main application file
- `run_hisab.sh` - Launcher script (Linux/macOS)
- `requirements.txt` - Documentation of requirements
- `README.md` - This documentation

## License

Open source - feel free to modify and distribute.