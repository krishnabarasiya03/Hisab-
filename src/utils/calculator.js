// Calculator utility functions for formula operations

export const getCellValue = (cellKey, cellData) => {
  const value = cellData[cellKey];
  if (value === null || value === undefined || value === '') return 0;
  
  if (typeof value === 'number') return value;
  
  // Try to parse as number
  const parsed = parseFloat(value);
  return isNaN(parsed) ? 0 : parsed;
};

export const parseFormula = (formula) => {
  const pattern = /^([A-Z])([+\-*/])([A-Z])$/;
  const match = formula.match(pattern);
  
  if (!match) {
    throw new Error('Invalid operation format. Use format like: C*D, A+B, etc.');
  }
  
  return {
    col1: match[1],
    operator: match[2],
    col2: match[3]
  };
};

export const executeFormula = (formula, cellData) => {
  const { col1, operator, col2 } = parseFormula(formula);
  
  const results = {};
  const resultCol = String.fromCharCode(Math.max(col1.charCodeAt(0), col2.charCodeAt(0)) + 1);
  
  // Perform operation for all rows (1 to 20)
  for (let row = 1; row <= 20; row++) {
    const cell1Key = `${col1}${row}`;
    const cell2Key = `${col2}${row}`;
    const resultKey = `${resultCol}${row}`;
    
    const val1 = getCellValue(cell1Key, cellData);
    const val2 = getCellValue(cell2Key, cellData);
    
    // Skip if both values are 0 (empty cells)
    if (val1 === 0 && val2 === 0) {
      continue;
    }
    
    let result;
    switch (operator) {
      case '+':
        result = val1 + val2;
        break;
      case '-':
        result = val1 - val2;
        break;
      case '*':
        result = val1 * val2;
        break;
      case '/':
        result = val2 !== 0 ? val1 / val2 : 0;
        break;
      default:
        throw new Error(`Unsupported operator: ${operator}`);
    }
    
    // Only set result if result column is valid (A-J)
    if (resultCol <= 'J') {
      results[resultKey] = result;
    }
  }
  
  return results;
};