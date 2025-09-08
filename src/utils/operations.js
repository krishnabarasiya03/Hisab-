// Utility functions for row and column operations

import { getCellValue } from './calculator.js';

export const performColumnOperation = (col, operation, value, cellData, maxRows) => {
  const colLetter = String.fromCharCode(65 + col);
  const updates = {};
  let message = '';
  
  // Get all values in the column
  const values = [];
  for (let row = 1; row <= maxRows; row++) {
    const cellKey = `${colLetter}${row}`;
    const cellValue = getCellValue(cellKey, cellData);
    if (cellValue !== 0) {
      values.push({ row, value: cellValue });
    }
  }
  
  if (operation === 'sum') {
    const sum = values.reduce((total, item) => total + item.value, 0);
    
    // Put result in the last used row + 1
    const lastRow = values.length > 0 ? Math.max(...values.map(v => v.row)) : 0;
    const resultKey = `${colLetter}${lastRow + 2}`;
    updates[resultKey] = sum;
    message = `Sum of column ${colLetter}: ${sum}`;
    
  } else if (['add', 'subtract', 'multiply', 'divide'].includes(operation)) {
    if (value === null || isNaN(value)) {
      throw new Error('Invalid value for operation');
    }
    
    values.forEach(({ row }) => {
      const cellKey = `${colLetter}${row}`;
      const currentValue = getCellValue(cellKey, cellData);
      
      let newValue;
      switch (operation) {
        case 'add':
          newValue = currentValue + value;
          break;
        case 'subtract':
          newValue = currentValue - value;
          break;
        case 'multiply':
          newValue = currentValue * value;
          break;
        case 'divide':
          newValue = value !== 0 ? currentValue / value : currentValue;
          break;
        default:
          throw new Error(`Unsupported operation: ${operation}`);
      }
      
      updates[cellKey] = newValue;
    });
    
    message = `Applied ${operation} ${value} to column ${colLetter}`;
  }
  
  return { updates, message };
};

export const performRowOperation = (row, operation, value, cellData, maxCols) => {
  const rowNum = row + 1;
  const updates = {};
  let message = '';
  
  // Get all values in the row
  const values = [];
  for (let col = 0; col < maxCols; col++) {
    const colLetter = String.fromCharCode(65 + col);
    const cellKey = `${colLetter}${rowNum}`;
    const cellValue = getCellValue(cellKey, cellData);
    if (cellValue !== 0) {
      values.push({ col, colLetter, value: cellValue });
    }
  }
  
  if (operation === 'sum') {
    const sum = values.reduce((total, item) => total + item.value, 0);
    
    // Put result in the next available column
    const lastCol = values.length > 0 ? Math.max(...values.map(v => v.col)) : -1;
    if (lastCol + 1 < maxCols) {
      const resultColLetter = String.fromCharCode(65 + lastCol + 1);
      const resultKey = `${resultColLetter}${rowNum}`;
      updates[resultKey] = sum;
    }
    message = `Sum of row ${rowNum}: ${sum}`;
    
  } else if (['add', 'subtract', 'multiply', 'divide'].includes(operation)) {
    if (value === null || isNaN(value)) {
      throw new Error('Invalid value for operation');
    }
    
    values.forEach(({ colLetter }) => {
      const cellKey = `${colLetter}${rowNum}`;
      const currentValue = getCellValue(cellKey, cellData);
      
      let newValue;
      switch (operation) {
        case 'add':
          newValue = currentValue + value;
          break;
        case 'subtract':
          newValue = currentValue - value;
          break;
        case 'multiply':
          newValue = currentValue * value;
          break;
        case 'divide':
          newValue = value !== 0 ? currentValue / value : currentValue;
          break;
        default:
          throw new Error(`Unsupported operation: ${operation}`);
      }
      
      updates[cellKey] = newValue;
    });
    
    message = `Applied ${operation} ${value} to row ${rowNum}`;
  }
  
  return { updates, message };
};