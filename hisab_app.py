#!/usr/bin/env python3
"""
Hisab Desktop Application
A simple Excel-like calculator with spreadsheet functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
import math
import csv
import os
import zipfile
import webbrowser
import urllib.parse
from datetime import datetime

class HisabApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hisab - Desktop Calculator")
        self.root.geometry("800x600")
        
        # Grid dimensions
        self.rows = 20
        self.cols = 10
        
        # Data storage for cell values
        self.cell_data = {}
        
        # Create the UI
        self.create_widgets()
        self.setup_grid()
        
    def create_widgets(self):
        """Create the main UI components"""
        
        # Top frame for operation input
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(top_frame, text="Operation:").pack(side=tk.LEFT)
        
        self.operation_var = tk.StringVar()
        self.operation_entry = ttk.Entry(top_frame, textvariable=self.operation_var, width=30)
        self.operation_entry.pack(side=tk.LEFT, padx=(5, 5))
        self.operation_entry.bind('<Return>', self.execute_operation)
        
        ttk.Button(top_frame, text="Execute", command=self.execute_operation).pack(side=tk.LEFT)
        ttk.Button(top_frame, text="Clear All", command=self.clear_all).pack(side=tk.LEFT, padx=(5, 0))
        ttk.Button(top_frame, text="Share via WhatsApp", command=self.share_via_whatsapp).pack(side=tk.LEFT, padx=(5, 0))
        
        # Main frame for the spreadsheet
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create canvas and scrollbars for the grid
        self.canvas = tk.Canvas(main_frame)
        v_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and canvas
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
    def setup_grid(self):
        """Create the Excel-like grid"""
        
        # Column headers (A, B, C, D, ...)
        for col in range(self.cols):
            col_letter = chr(65 + col)  # A=65, B=66, etc.
            header_label = tk.Label(self.scrollable_frame, text=col_letter, 
                                  bg='lightgray', relief=tk.RAISED, width=8)
            header_label.grid(row=0, column=col+1, sticky='nsew')
            
            # Bind right-click for column operations
            header_label.bind("<Button-3>", lambda e, c=col: self.show_column_menu(e, c))
        
        # Row headers and cells
        self.cells = {}
        for row in range(self.rows):
            # Row header (1, 2, 3, ...)
            row_header = tk.Label(self.scrollable_frame, text=str(row+1), 
                                bg='lightgray', relief=tk.RAISED, width=3)
            row_header.grid(row=row+1, column=0, sticky='nsew')
            
            # Bind right-click for row operations
            row_header.bind("<Button-3>", lambda e, r=row: self.show_row_menu(e, r))
            
            # Create cells
            for col in range(self.cols):
                cell_key = f"{chr(65 + col)}{row + 1}"
                
                cell_var = tk.StringVar()
                cell_entry = tk.Entry(self.scrollable_frame, textvariable=cell_var, width=10)
                cell_entry.grid(row=row+1, column=col+1, padx=1, pady=1, sticky='nsew')
                
                # Store references
                self.cells[cell_key] = {
                    'widget': cell_entry,
                    'var': cell_var
                }
                
                # Bind events
                cell_var.trace('w', lambda *args, key=cell_key: self.on_cell_change(key))
    
    def on_cell_change(self, cell_key):
        """Handle cell value changes"""
        value = self.cells[cell_key]['var'].get()
        try:
            # Try to convert to number
            self.cell_data[cell_key] = float(value) if '.' in value else int(value)
        except ValueError:
            # Store as string if not a number
            self.cell_data[cell_key] = value
    
    def get_cell_value(self, cell_key):
        """Get numeric value from a cell"""
        if cell_key in self.cell_data:
            value = self.cell_data[cell_key]
            if isinstance(value, (int, float)):
                return value
            try:
                return float(value) if '.' in str(value) else int(value)
            except ValueError:
                return 0
        return 0
    
    def set_cell_value(self, cell_key, value):
        """Set value in a cell"""
        if cell_key in self.cells:
            self.cells[cell_key]['var'].set(str(value))
    
    def execute_operation(self, event=None):
        """Execute the operation entered in the operation field"""
        operation = self.operation_var.get().strip().upper()
        
        if not operation:
            return
        
        try:
            # Parse operation like "C*D" or "A+B"
            pattern = r'([A-Z])([+\-*/])([A-Z])'
            match = re.match(pattern, operation)
            
            if not match:
                messagebox.showerror("Error", "Invalid operation format. Use format like: C*D, A+B, etc.")
                return
            
            col1, operator, col2 = match.groups()
            
            # Perform operation for all rows
            for row in range(1, self.rows + 1):
                cell1_key = f"{col1}{row}"
                cell2_key = f"{col2}{row}"
                result_col = chr(ord(max(col1, col2)) + 1)  # Next column after the operands
                result_key = f"{result_col}{row}"
                
                val1 = self.get_cell_value(cell1_key)
                val2 = self.get_cell_value(cell2_key)
                
                # Skip if both values are 0 (empty cells)
                if val1 == 0 and val2 == 0:
                    continue
                
                # Calculate result
                if operator == '+':
                    result = val1 + val2
                elif operator == '-':
                    result = val1 - val2
                elif operator == '*':
                    result = val1 * val2
                elif operator == '/':
                    result = val1 / val2 if val2 != 0 else 0
                
                # Set result in the next column
                if result_col in [chr(65 + i) for i in range(self.cols)]:
                    self.set_cell_value(result_key, result)
            
            messagebox.showinfo("Success", f"Operation {operation} executed successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error executing operation: {str(e)}")
    
    def show_column_menu(self, event, col):
        """Show context menu for column operations"""
        menu = tk.Menu(self.root, tearoff=0)
        col_letter = chr(65 + col)
        
        menu.add_command(label=f"Sum Column {col_letter}", 
                        command=lambda: self.column_operation(col, 'sum'))
        menu.add_command(label=f"Multiply Column {col_letter}", 
                        command=lambda: self.column_operation(col, 'multiply'))
        menu.add_command(label=f"Add to Column {col_letter}", 
                        command=lambda: self.column_operation(col, 'add'))
        menu.add_command(label=f"Subtract from Column {col_letter}", 
                        command=lambda: self.column_operation(col, 'subtract'))
        menu.add_command(label=f"Divide Column {col_letter}", 
                        command=lambda: self.column_operation(col, 'divide'))
        menu.add_separator()
        menu.add_command(label=f"Clear Column {col_letter}", 
                        command=lambda: self.clear_column(col))
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def show_row_menu(self, event, row):
        """Show context menu for row operations"""
        menu = tk.Menu(self.root, tearoff=0)
        row_num = row + 1
        
        menu.add_command(label=f"Sum Row {row_num}", 
                        command=lambda: self.row_operation(row, 'sum'))
        menu.add_command(label=f"Multiply Row {row_num}", 
                        command=lambda: self.row_operation(row, 'multiply'))
        menu.add_command(label=f"Add to Row {row_num}", 
                        command=lambda: self.row_operation(row, 'add'))
        menu.add_command(label=f"Subtract from Row {row_num}", 
                        command=lambda: self.row_operation(row, 'subtract'))
        menu.add_command(label=f"Divide Row {row_num}", 
                        command=lambda: self.row_operation(row, 'divide'))
        menu.add_separator()
        menu.add_command(label=f"Clear Row {row_num}", 
                        command=lambda: self.clear_row(row))
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def column_operation(self, col, operation):
        """Perform operation on entire column"""
        col_letter = chr(65 + col)
        
        if operation in ['add', 'subtract', 'multiply', 'divide']:
            # Get value from user
            from tkinter import simpledialog
            value = simpledialog.askfloat("Input", f"Enter value to {operation}:")
            if value is None:
                return
        
        values = []
        for row in range(1, self.rows + 1):
            cell_key = f"{col_letter}{row}"
            cell_value = self.get_cell_value(cell_key)
            if cell_value != 0:  # Only include non-empty cells
                values.append(cell_value)
        
        if not values and operation != 'sum':
            messagebox.showwarning("Warning", "No values found in column!")
            return
        
        if operation == 'sum':
            result = sum(values)
            # Put result in the last used row + 1
            last_row = len([v for v in values if v != 0])
            result_key = f"{col_letter}{last_row + 2}"
            self.set_cell_value(result_key, result)
            messagebox.showinfo("Result", f"Sum of column {col_letter}: {result}")
        
        elif operation in ['add', 'subtract', 'multiply', 'divide']:
            for row in range(1, self.rows + 1):
                cell_key = f"{col_letter}{row}"
                current_value = self.get_cell_value(cell_key)
                if current_value != 0:  # Only modify non-empty cells
                    if operation == 'add':
                        new_value = current_value + value
                    elif operation == 'subtract':
                        new_value = current_value - value
                    elif operation == 'multiply':
                        new_value = current_value * value
                    elif operation == 'divide':
                        new_value = current_value / value if value != 0 else current_value
                    
                    self.set_cell_value(cell_key, new_value)
    
    def row_operation(self, row, operation):
        """Perform operation on entire row"""
        row_num = row + 1
        
        if operation in ['add', 'subtract', 'multiply', 'divide']:
            # Get value from user
            from tkinter import simpledialog
            value = simpledialog.askfloat("Input", f"Enter value to {operation}:")
            if value is None:
                return
        
        values = []
        for col in range(self.cols):
            col_letter = chr(65 + col)
            cell_key = f"{col_letter}{row_num}"
            cell_value = self.get_cell_value(cell_key)
            if cell_value != 0:  # Only include non-empty cells
                values.append(cell_value)
        
        if not values and operation != 'sum':
            messagebox.showwarning("Warning", "No values found in row!")
            return
        
        if operation == 'sum':
            result = sum(values)
            # Put result in the next available column
            last_col = len([v for v in values if v != 0])
            if last_col < self.cols:
                result_col = chr(65 + last_col + 1)
                result_key = f"{result_col}{row_num}"
                self.set_cell_value(result_key, result)
            messagebox.showinfo("Result", f"Sum of row {row_num}: {result}")
        
        elif operation in ['add', 'subtract', 'multiply', 'divide']:
            for col in range(self.cols):
                col_letter = chr(65 + col)
                cell_key = f"{col_letter}{row_num}"
                current_value = self.get_cell_value(cell_key)
                if current_value != 0:  # Only modify non-empty cells
                    if operation == 'add':
                        new_value = current_value + value
                    elif operation == 'subtract':
                        new_value = current_value - value
                    elif operation == 'multiply':
                        new_value = current_value * value
                    elif operation == 'divide':
                        new_value = current_value / value if value != 0 else current_value
                    
                    self.set_cell_value(cell_key, new_value)
    
    def clear_column(self, col):
        """Clear all values in a column"""
        col_letter = chr(65 + col)
        for row in range(1, self.rows + 1):
            cell_key = f"{col_letter}{row}"
            self.set_cell_value(cell_key, "")
        if col_letter in self.cell_data:
            del self.cell_data[col_letter]
    
    def clear_row(self, row):
        """Clear all values in a row"""
        row_num = row + 1
        for col in range(self.cols):
            col_letter = chr(65 + col)
            cell_key = f"{col_letter}{row_num}"
            self.set_cell_value(cell_key, "")
            if cell_key in self.cell_data:
                del self.cell_data[cell_key]
    
    def clear_all(self):
        """Clear all data in the spreadsheet"""
        for cell_key in self.cells:
            self.set_cell_value(cell_key, "")
        self.cell_data.clear()
        self.operation_var.set("")
    
    def export_data_to_csv(self, filename):
        """Export current spreadsheet data to CSV file"""
        # Determine the actual data range (non-empty cells)
        max_row = 0
        max_col = 0
        
        for cell_key in self.cell_data:
            if self.cell_data[cell_key]:  # Non-empty cell
                # Parse cell key like "A1", "B5", etc.
                col_letter = cell_key[0]
                row_num = int(cell_key[1:])
                col_num = ord(col_letter) - ord('A')
                
                max_row = max(max_row, row_num)
                max_col = max(max_col, col_num)
        
        if max_row == 0 and max_col == 0:
            # No data to export
            return False
        
        # Create CSV data
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header row with column letters
            header = [''] + [chr(65 + col) for col in range(max_col + 1)]
            writer.writerow(header)
            
            # Write data rows
            for row in range(1, max_row + 1):
                row_data = [str(row)]  # Row number
                for col in range(max_col + 1):
                    col_letter = chr(65 + col)
                    cell_key = f"{col_letter}{row}"
                    value = self.cell_data.get(cell_key, "")
                    row_data.append(str(value) if value else "")
                writer.writerow(row_data)
        
        return True
    
    def create_share_zip(self):
        """Create a zip file with the spreadsheet data"""
        # Generate timestamp for unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"Hisab_Data_{timestamp}.zip"
        csv_filename = f"Hisab_Spreadsheet_{timestamp}.csv"
        
        # Create temporary CSV file
        temp_csv_path = os.path.join(os.path.dirname(__file__), csv_filename)
        
        # Export data to CSV
        if not self.export_data_to_csv(temp_csv_path):
            return None, "No data to export. Please enter some data in the spreadsheet first."
        
        # Create zip file
        zip_path = os.path.join(os.path.dirname(__file__), zip_filename)
        
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(temp_csv_path, csv_filename)
                
                # Add a readme file with instructions
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
            
            # Clean up temporary CSV file
            os.remove(temp_csv_path)
            
            return zip_path, None
        
        except Exception as e:
            # Clean up on error
            if os.path.exists(temp_csv_path):
                os.remove(temp_csv_path)
            return None, f"Error creating zip file: {str(e)}"
    
    def share_via_whatsapp(self):
        """Share spreadsheet data via WhatsApp"""
        try:
            # Create zip file
            zip_path, error = self.create_share_zip()
            
            if error:
                messagebox.showwarning("No Data", error)
                return
            
            if not zip_path:
                messagebox.showerror("Error", "Failed to create share file")
                return
            
            # Get file size for display
            file_size = os.path.getsize(zip_path)
            file_size_kb = file_size / 1024
            
            # Create WhatsApp message
            message = f"📊 Sharing my Hisab spreadsheet data!\n\n" \
                     f"File: {os.path.basename(zip_path)}\n" \
                     f"Size: {file_size_kb:.1f} KB\n" \
                     f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n" \
                     f"Open the attached CSV file in any spreadsheet app.\n\n" \
                     f"🧮 Get Hisab Calculator: https://github.com/krishnabarasiya03/Hisab-"
            
            # URL encode the message
            encoded_message = urllib.parse.quote(message)
            
            # WhatsApp Web URL
            whatsapp_url = f"https://web.whatsapp.com/send?text={encoded_message}"
            
            # Show success dialog with options
            result = messagebox.askyesnocancel(
                "Share via WhatsApp", 
                f"✅ Zip file created successfully!\n\n"
                f"File: {os.path.basename(zip_path)}\n"
                f"Location: {zip_path}\n"
                f"Size: {file_size_kb:.1f} KB\n\n"
                f"Click 'Yes' to open WhatsApp Web\n"
                f"Click 'No' to just keep the file\n"
                f"Click 'Cancel' to delete the file"
            )
            
            if result is True:  # Yes - Open WhatsApp
                webbrowser.open(whatsapp_url)
                messagebox.showinfo(
                    "Next Steps", 
                    "1. WhatsApp Web is opening in your browser\n"
                    "2. Manually attach the zip file to your message\n"
                    "3. The message text is pre-filled for you\n\n"
                    f"Zip file location:\n{zip_path}"
                )
            elif result is False:  # No - Keep file
                messagebox.showinfo(
                    "File Saved", 
                    f"Your spreadsheet data has been saved to:\n{zip_path}\n\n"
                    f"You can manually share this file via any method."
                )
            else:  # Cancel - Delete file
                os.remove(zip_path)
                messagebox.showinfo("Cancelled", "Share cancelled and file deleted.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error sharing via WhatsApp: {str(e)}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = HisabApp(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()