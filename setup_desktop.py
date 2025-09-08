#!/usr/bin/env python3
"""
Desktop Setup Script for Hisab Calculator
Automatically creates desktop shortcuts and application menu entries
JavaScript/React/Electron version only
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def get_script_dir():
    """Get the directory where this script is located"""
    return Path(__file__).parent.absolute()

def detect_version():
    """Detect which version of Hisab is available"""
    script_dir = get_script_dir()
    
    has_js = (script_dir / "package.json").exists()
    
    if has_js:
        return "javascript"
    else:
        return "unknown"

def create_linux_desktop_entry():
    """Create desktop entry for Linux systems"""
    script_dir = get_script_dir()
    
    launcher_path = script_dir / "run_hisab.sh"
    comment = "Excel-like desktop calculator with React and Electron"
    categories = "Office;Calculator;Development;"
    
    # Make sure the launcher script is executable
    os.chmod(launcher_path, 0o755)
    
    desktop_entry_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Hisab Calculator
Comment={comment}
Exec={launcher_path}
Icon=calc
Terminal=false
Categories={categories}
StartupNotify=true
"""
    
    # Create desktop entry in applications directory
    apps_dir = Path.home() / ".local" / "share" / "applications"
    apps_dir.mkdir(parents=True, exist_ok=True)
    
    desktop_file = apps_dir / "hisab.desktop"
    with open(desktop_file, 'w') as f:
        f.write(desktop_entry_content)
    
    os.chmod(desktop_file, 0o755)
    print(f"✓ Created application menu entry: {desktop_file}")
    
    # Optionally create desktop shortcut
    desktop_dir = Path.home() / "Desktop"
    if desktop_dir.exists():
        desktop_shortcut = desktop_dir / "hisab.desktop"
        with open(desktop_shortcut, 'w') as f:
            f.write(desktop_entry_content)
        
        os.chmod(desktop_shortcut, 0o755)
        print(f"✓ Created desktop shortcut: {desktop_shortcut}")
    
    print(f"\n📋 Linux Setup Complete! ({version} version)")
    print("- Hisab Calculator is now available in your applications menu under 'Office'")
    if desktop_dir.exists():
        print("- Desktop shortcut created")
    print("- You can also run: ./run_hisab.sh")

def create_windows_shortcuts():
    """Create shortcuts for Windows"""
    version = detect_version()
    
    print(f"\n🪟 Windows Setup Instructions ({version} version):")
    print("To create desktop shortcuts on Windows:")
    print("1. Right-click on 'run_hisab.bat' in the file explorer")
    print("2. Select 'Send to' → 'Desktop (create shortcut)'")
    print("3. Rename the shortcut to 'Hisab Calculator'")
    print("\nTo add to Start Menu:")
    print("1. Copy the desktop shortcut")
    print("2. Paste it in: %APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\")
    
    if version == "javascript":
        print("\nFor JavaScript/Electron version:")
        print("- Requires Node.js 16+ to be installed")
        print("- First run will install dependencies automatically")
        print("- You can also use: npm run dist to create installer packages")
    else:
        print("\nFor Python version:")
        print("- Requires Python 3.6+ with tkinter")
    
    print("\nAlternatively, double-click 'run_hisab.bat' to run the application.")

def create_macos_instructions():
    """Provide instructions for macOS"""
    script_dir = get_script_dir()
    launcher_path = script_dir / "run_hisab.sh"
    version = detect_version()
    
    # Make sure the launcher script is executable
    os.chmod(launcher_path, 0o755)
    
    print(f"\n🍎 macOS Setup Instructions ({version} version):")
    print("To create an application bundle:")
    print("1. Open Automator")
    print("2. Choose 'Application'")
    print("3. Add 'Run Shell Script' action")
    print(f"4. Enter this path: {launcher_path}")
    print("5. Save as 'Hisab Calculator.app' in Applications folder")
    print("\nTo create desktop alias:")
    print("1. Drag the app from Applications to Desktop while holding ⌥+⌘")
    
    if version == "javascript":
        print("\nFor JavaScript/Electron version:")
        print("- Requires Node.js 16+ (install via Homebrew: brew install node)")
        print("- You can also use: npm run dist to create .dmg installer")
    else:
        print("\nFor Python version:")
        print("- Requires Python 3.6+ with tkinter")
    
    print(f"\nAlternatively, run directly: {launcher_path}")

def main():
    version = detect_version()
    
    print("🧮 Hisab Calculator - Desktop Setup Utility")
    print("=" * 50)
    print(f"Detected version: {version.upper()}")
    
    if version == "unknown":
        print("❌ Could not detect Hisab Calculator version!")
        print("Make sure you're running this script from the Hisab directory.")
        return
    
    system = platform.system().lower()
    
    if system == "linux":
        try:
            create_linux_desktop_entry()
        except Exception as e:
            print(f"❌ Error creating Linux desktop entry: {e}")
            print("You can manually run: ./run_hisab.sh")
    
    elif system == "windows":
        create_windows_shortcuts()
    
    elif system == "darwin":  # macOS
        create_macos_instructions()
    
    else:
        print(f"❓ Unknown system: {system}")
        print("Please refer to the README.md for manual setup instructions.")
    
    print("\n" + "=" * 50)
    print("Setup complete! You can now:")
    print("• Find Hisab Calculator in your applications menu")
    print("• Use desktop shortcuts (if created)")
    print("• Run directly: npm start (after npm install && npm run build)")
    print("• Development mode: npm run dev")
    
    print("\nFor troubleshooting, see README.md")

if __name__ == "__main__":
    main()