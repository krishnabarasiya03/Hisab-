#!/usr/bin/env python3
"""
Desktop Setup Script for Hisab Calculator
Automatically creates desktop shortcuts and application menu entries
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def get_script_dir():
    """Get the directory where this script is located"""
    return Path(__file__).parent.absolute()

def create_linux_desktop_entry():
    """Create desktop entry for Linux systems"""
    script_dir = get_script_dir()
    launcher_path = script_dir / "run_hisab.sh"
    
    # Make sure the launcher script is executable
    os.chmod(launcher_path, 0o755)
    
    desktop_entry_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Hisab Calculator
Comment=Excel-like desktop calculator with spreadsheet functionality
Exec={launcher_path}
Icon=calc
Terminal=false
Categories=Office;Calculator;
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
    
    print("\n📋 Linux Setup Complete!")
    print("- Hisab Calculator is now available in your applications menu under 'Office'")
    if desktop_dir.exists():
        print("- Desktop shortcut created")
    print("- You can also run: ./run_hisab.sh")

def create_windows_shortcuts():
    """Create shortcuts for Windows"""
    print("\n🪟 Windows Setup Instructions:")
    print("To create desktop shortcuts on Windows:")
    print("1. Right-click on 'run_hisab.bat' in the file explorer")
    print("2. Select 'Send to' → 'Desktop (create shortcut)'")
    print("3. Rename the shortcut to 'Hisab Calculator'")
    print("\nTo add to Start Menu:")
    print("1. Copy the desktop shortcut")
    print("2. Paste it in: %APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\")
    print("\nAlternatively, double-click 'run_hisab.bat' to run the application.")

def create_macos_instructions():
    """Provide instructions for macOS"""
    script_dir = get_script_dir()
    launcher_path = script_dir / "run_hisab.sh"
    
    # Make sure the launcher script is executable
    os.chmod(launcher_path, 0o755)
    
    print("\n🍎 macOS Setup Instructions:")
    print("To create an application bundle:")
    print("1. Open Automator")
    print("2. Choose 'Application'")
    print("3. Add 'Run Shell Script' action")
    print(f"4. Enter this path: {launcher_path}")
    print("5. Save as 'Hisab Calculator.app' in Applications folder")
    print("\nTo create desktop alias:")
    print("1. Drag the app from Applications to Desktop while holding ⌥+⌘")
    print(f"\nAlternatively, run directly: {launcher_path}")

def main():
    print("🧮 Hisab Calculator - Desktop Setup Utility")
    print("=" * 50)
    
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
    print("• Run directly: python3 hisab_app.py")
    print("\nFor troubleshooting, see README.md")

if __name__ == "__main__":
    main()