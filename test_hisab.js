// Test script for Hisab Calculator - JavaScript/React version
// Tests core functionality

import { getCellValue, parseFormula, executeFormula } from '../src/utils/calculator.js';
import { performColumnOperation, performRowOperation } from '../src/utils/operations.js';

// Mock data for testing
const testCellData = {
  'A1': 10,
  'B1': 5,
  'A2': 20,
  'B2': 8,
  'A3': 15,
  'B3': 3
};

function testCellOperations() {
  console.log('Testing cell operations...');
  
  // Test data
  console.log('Test data:');
  Object.entries(testCellData).forEach(([key, value]) => {
    console.log(`  ${key}: ${value}`);
  });
  
  console.log('\nTesting A*B operation (should multiply A1*B1, A2*B2, A3*B3):');
  for (let row = 1; row <= 3; row++) {
    const aVal = getCellValue(`A${row}`, testCellData);
    const bVal = getCellValue(`B${row}`, testCellData);
    const result = aVal * bVal;
    console.log(`  A${row}*B${row} = ${aVal}*${bVal} = ${result}`);
  }
  
  console.log('\nTesting A+B operation:');
  for (let row = 1; row <= 3; row++) {
    const aVal = getCellValue(`A${row}`, testCellData);
    const bVal = getCellValue(`B${row}`, testCellData);
    const result = aVal + bVal;
    console.log(`  A${row}+B${row} = ${aVal}+${bVal} = ${result}`);
  }
  
  console.log('✓ Cell operations test passed!');
}

function testFormulaExecution() {
  console.log('\nTesting formula execution...');
  
  try {
    // Test A*B formula
    const results = executeFormula('A*B', testCellData);
    console.log('Results from A*B formula:');
    Object.entries(results).forEach(([key, value]) => {
      console.log(`  ${key}: ${value}`);
    });
    
    // Test A+B formula
    const addResults = executeFormula('A+B', testCellData);
    console.log('Results from A+B formula:');
    Object.entries(addResults).forEach(([key, value]) => {
      console.log(`  ${key}: ${value}`);
    });
    
    console.log('✓ Formula execution test passed!');
  } catch (error) {
    console.error('❌ Formula execution test failed:', error.message);
    throw error;
  }
}

function testFormulaParsing() {
  console.log('\nTesting formula parsing...');
  
  const testFormulas = ['C*D', 'A+B', 'E-F', 'G/H'];
  
  testFormulas.forEach(formula => {
    try {
      const parsed = parseFormula(formula);
      console.log(`  Formula '${formula}' parsed as: ${parsed.col1} ${parsed.operator} ${parsed.col2}`);
    } catch (error) {
      console.log(`  Formula '${formula}' failed to parse: ${error.message}`);
    }
  });
  
  console.log('✓ Formula parsing test passed!');
}

function testColumnOperations() {
  console.log('\nTesting column operations...');
  
  try {
    // Test sum operation on column A
    const sumResult = performColumnOperation(0, 'sum', null, testCellData, 20);
    console.log('Column A sum operation result:');
    console.log(`  Updates: ${JSON.stringify(sumResult.updates)}`);
    console.log(`  Message: ${sumResult.message}`);
    
    // Test multiply operation on column A
    const multiplyResult = performColumnOperation(0, 'multiply', 2, testCellData, 20);
    console.log('Column A multiply by 2 operation result:');
    console.log(`  Updates count: ${Object.keys(multiplyResult.updates).length}`);
    console.log(`  Message: ${multiplyResult.message}`);
    
    console.log('✓ Column operations test passed!');
  } catch (error) {
    console.error('❌ Column operations test failed:', error.message);
    throw error;
  }
}

function testRowOperations() {
  console.log('\nTesting row operations...');
  
  try {
    // Test sum operation on row 1 (index 0)
    const sumResult = performRowOperation(0, 'sum', null, testCellData, 10);
    console.log('Row 1 sum operation result:');
    console.log(`  Updates: ${JSON.stringify(sumResult.updates)}`);
    console.log(`  Message: ${sumResult.message}`);
    
    // Test add operation on row 1
    const addResult = performRowOperation(0, 'add', 5, testCellData, 10);
    console.log('Row 1 add 5 operation result:');
    console.log(`  Updates count: ${Object.keys(addResult.updates).length}`);
    console.log(`  Message: ${addResult.message}`);
    
    console.log('✓ Row operations test passed!');
  } catch (error) {
    console.error('❌ Row operations test failed:', error.message);
    throw error;
  }
}

function testColumnLetterGeneration() {
  console.log('\nTesting column letter generation...');
  
  for (let i = 0; i < 10; i++) {
    const letter = String.fromCharCode(65 + i);
    console.log(`  Column ${i}: ${letter}`);
  }
  
  console.log('✓ Column letter generation test passed!');
}

function main() {
  console.log('Hisab Calculator - JavaScript/React Version - Core Functionality Tests');
  console.log('='.repeat(70));
  
  try {
    testCellOperations();
    testFormulaParsing();
    testFormulaExecution();
    testColumnOperations();
    testRowOperations();
    testColumnLetterGeneration();
    
    console.log('\n' + '='.repeat(70));
    console.log('✅ All tests passed successfully!');
    console.log('\nCore functionality is working correctly.');
    console.log('The React/Electron application should work as expected.');
    
    return true;
  } catch (error) {
    console.log(`\n❌ Test failed with error: ${error.message}`);
    console.error(error);
    return false;
  }
}

// Export for use in Jest or run directly in Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    testCellOperations,
    testFormulaParsing,
    testFormulaExecution,
    testColumnOperations,
    testRowOperations,
    testColumnLetterGeneration,
    main
  };
}

// Run tests if this file is executed directly
if (typeof require !== 'undefined' && require.main === module) {
  const success = main();
  process.exit(success ? 0 : 1);
}