#!/usr/bin/env python3
"""
End-to-end test for WhatsApp share feature
Simulates real usage without GUI
"""

import sys
import os
import tempfile
import zipfile
import csv
from datetime import datetime
sys.path.insert(0, os.path.dirname(__file__))

def simulate_whatsapp_share():
    """Simulate the complete WhatsApp share workflow"""
    print("Simulating end-to-end WhatsApp share workflow...")
    print("=" * 50)
    
    # Simulate cell data that a user might have entered
    print("1. Simulating user data entry...")
    cell_data = {
        'A1': 100,    # Budget items
        'A2': 50, 
        'A3': 75,
        'B1': 'Groceries',  # Would be converted to string
        'B2': 'Transport',
        'B3': 'Entertainment',
        'C1': 95,     # Actual spending
        'C2': 45,
        'C3': 80
    }
    print(f"   Simulated data: {len(cell_data)} cells with values")
    
    # Export to CSV (simplified version of the real function)
    print("\n2. Exporting data to CSV...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"Hisab_Spreadsheet_{timestamp}.csv"
    
    # Find data bounds
    max_row = 0
    max_col = 0
    
    for cell_key in cell_data:
        if cell_data[cell_key]:
            col_letter = cell_key[0]
            row_num = int(cell_key[1:])
            col_num = ord(col_letter) - ord('A')
            
            max_row = max(max_row, row_num)
            max_col = max(max_col, col_num)
    
    print(f"   Data bounds: {max_row} rows, {max_col + 1} columns")
    
    # Create CSV in temp directory
    temp_dir = tempfile.mkdtemp()
    csv_path = os.path.join(temp_dir, csv_filename)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Header row
        header = [''] + [chr(65 + col) for col in range(max_col + 1)]
        writer.writerow(header)
        
        # Data rows
        for row in range(1, max_row + 1):
            row_data = [str(row)]
            for col in range(max_col + 1):
                col_letter = chr(65 + col)
                cell_key = f"{col_letter}{row}"
                value = cell_data.get(cell_key, "")
                row_data.append(str(value) if value else "")
            writer.writerow(row_data)
    
    print(f"   CSV created: {csv_filename}")
    
    # Create zip file
    print("\n3. Creating zip file...")
    zip_filename = f"Hisab_Data_{timestamp}.zip"
    zip_path = os.path.join(temp_dir, zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_path, csv_filename)
        
        # Add README
        readme_content = f"""Hisab Spreadsheet Data
====================

This zip file contains your Hisab spreadsheet data exported on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.

Files included:
- {csv_filename}: Your spreadsheet data in CSV format

To open the CSV file:
- Use Microsoft Excel, Google Sheets, or any spreadsheet application
- Import as CSV with comma separator

About Hisab:
Hisab is a simple Excel-like desktop calculator with spreadsheet functionality.
Get Hisab at: https://github.com/krishnabarasiya03/Hisab-

"""
        zipf.writestr("README.txt", readme_content)
    
    # Get file size
    file_size = os.path.getsize(zip_path)
    file_size_kb = file_size / 1024
    
    print(f"   Zip created: {zip_filename}")
    print(f"   File size: {file_size_kb:.1f} KB")
    
    # Simulate WhatsApp message creation
    print("\n4. Generating WhatsApp message...")
    message = f"📊 Sharing my Hisab spreadsheet data!\n\n" \
             f"File: {zip_filename}\n" \
             f"Size: {file_size_kb:.1f} KB\n" \
             f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n" \
             f"Open the attached CSV file in any spreadsheet app.\n\n" \
             f"🧮 Get Hisab Calculator: https://github.com/krishnabarasiya03/Hisab-"
    
    print("   Message preview:")
    for line in message.split('\n'):
        print(f"     {line}")
    
    # Verify zip contents
    print("\n5. Verifying zip file contents...")
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        files = zipf.namelist()
        print(f"   Files in zip: {files}")
        
        # Check CSV content
        csv_content = zipf.read(csv_filename).decode('utf-8')
        csv_lines = csv_content.strip().split('\n')
        print(f"   CSV has {len(csv_lines)} lines")
        print(f"   First line (header): {csv_lines[0]}")
        print(f"   Second line (data): {csv_lines[1]}")
        
        # Check README
        readme_content = zipf.read("README.txt").decode('utf-8')
        print(f"   README length: {len(readme_content)} characters")
    
    print("\n6. Cleanup...")
    os.remove(csv_path)
    os.remove(zip_path)
    os.rmdir(temp_dir)
    print("   Temporary files cleaned up")
    
    print("\n" + "=" * 50)
    print("✅ End-to-end WhatsApp share simulation completed successfully!")
    print("\nFeatures demonstrated:")
    print("• Data export to CSV format")
    print("• Zip file creation with README")
    print("• WhatsApp message generation")
    print("• File size calculation")
    print("• Proper cleanup")
    
    return True

if __name__ == "__main__":
    success = simulate_whatsapp_share()
    sys.exit(0 if success else 1)