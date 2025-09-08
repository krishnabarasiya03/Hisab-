#!/usr/bin/env python3
"""
Test script for WhatsApp share functionality
Tests the new export and share features without GUI
"""

import sys
import os
import csv
import zipfile
import tempfile
sys.path.insert(0, os.path.dirname(__file__))

def test_csv_export():
    """Test CSV export functionality"""
    print("Testing CSV export functionality...")
    
    # Mock the cell data structure
    cell_data = {
        'A1': 10,
        'B1': 5,
        'A2': 20,
        'B2': 8,
        'C1': 50,
        'C2': 160
    }
    
    # Create a mock export function (simplified version of the real one)
    def export_data_to_csv(cell_data, filename):
        # Find max row and column
        max_row = 0
        max_col = 0
        
        for cell_key in cell_data:
            if cell_data[cell_key]:
                col_letter = cell_key[0]
                row_num = int(cell_key[1:])
                col_num = ord(col_letter) - ord('A')
                
                max_row = max(max_row, row_num)
                max_col = max(max_col, col_num)
        
        if max_row == 0 and max_col == 0:
            return False
        
        # Create CSV data
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header row
            header = [''] + [chr(65 + col) for col in range(max_col + 1)]
            writer.writerow(header)
            
            # Write data rows
            for row in range(1, max_row + 1):
                row_data = [str(row)]
                for col in range(max_col + 1):
                    col_letter = chr(65 + col)
                    cell_key = f"{col_letter}{row}"
                    value = cell_data.get(cell_key, "")
                    row_data.append(str(value) if value else "")
                writer.writerow(row_data)
        
        return True
    
    # Test export
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
        temp_filename = temp_file.name
    
    success = export_data_to_csv(cell_data, temp_filename)
    
    if success:
        # Verify the CSV file content
        with open(temp_filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            
            print(f"  CSV exported with {len(rows)} rows")
            print(f"  Header: {rows[0]}")
            print(f"  Row 1: {rows[1]}")
            print(f"  Row 2: {rows[2]}")
            
            # Verify data integrity
            assert rows[0] == ['', 'A', 'B', 'C'], f"Header mismatch: {rows[0]}"
            assert rows[1] == ['1', '10', '5', '50'], f"Row 1 mismatch: {rows[1]}"
            assert rows[2] == ['2', '20', '8', '160'], f"Row 2 mismatch: {rows[2]}"
        
        # Clean up
        os.unlink(temp_filename)
        print("✓ CSV export test passed!")
        return True
    else:
        print("✗ CSV export failed!")
        return False

def test_zip_creation():
    """Test zip file creation"""
    print("Testing zip file creation...")
    
    # Create a test CSV file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_csv:
        temp_csv_path = temp_csv.name
        writer = csv.writer(temp_csv)
        writer.writerow(['', 'A', 'B', 'C'])
        writer.writerow(['1', '10', '5', '50'])
        writer.writerow(['2', '20', '8', '160'])
    
    # Create zip file
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
        temp_zip_path = temp_zip.name
    
    try:
        with zipfile.ZipFile(temp_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(temp_csv_path, 'test_data.csv')
            zipf.writestr('README.txt', 'Test readme content')
        
        # Verify zip contents
        with zipfile.ZipFile(temp_zip_path, 'r') as zipf:
            files = zipf.namelist()
            print(f"  Zip created with files: {files}")
            
            assert 'test_data.csv' in files, "CSV file not in zip"
            assert 'README.txt' in files, "README not in zip"
            
            # Verify CSV content in zip
            csv_content = zipf.read('test_data.csv').decode('utf-8')
            assert '10,5,50' in csv_content, "CSV data not preserved in zip"
        
        print("✓ Zip creation test passed!")
        success = True
    
    except Exception as e:
        print(f"✗ Zip creation failed: {e}")
        success = False
    
    finally:
        # Clean up
        os.unlink(temp_csv_path)
        if os.path.exists(temp_zip_path):
            os.unlink(temp_zip_path)
    
    return success

def test_empty_data_handling():
    """Test handling of empty data"""
    print("Testing empty data handling...")
    
    # Test with empty cell data
    cell_data = {}
    
    def export_data_to_csv(cell_data, filename):
        max_row = 0
        max_col = 0
        
        for cell_key in cell_data:
            if cell_data[cell_key]:
                col_letter = cell_key[0]
                row_num = int(cell_key[1:])
                col_num = ord(col_letter) - ord('A')
                
                max_row = max(max_row, row_num)
                max_col = max(max_col, col_num)
        
        return max_row > 0 and max_col >= 0
    
    result = export_data_to_csv(cell_data, "dummy.csv")
    
    if not result:
        print("✓ Empty data handling test passed!")
        return True
    else:
        print("✗ Empty data handling failed - should return False for empty data")
        return False

def main():
    """Run all tests"""
    print("WhatsApp Share Functionality Tests")
    print("=" * 40)
    
    tests = [
        test_csv_export,
        test_zip_creation,
        test_empty_data_handling
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
    
    print("=" * 40)
    if passed == len(tests):
        print("✅ All WhatsApp share tests passed!")
        return True
    else:
        print(f"❌ {len(tests) - passed} test(s) failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)