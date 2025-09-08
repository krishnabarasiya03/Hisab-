import React, { useState, useCallback } from 'react';
import './App.css';
import SpreadsheetGrid from './components/SpreadsheetGrid';
import OperationBar from './components/OperationBar';
import { executeFormula } from './utils/calculator';

function App() {
  const [cellData, setCellData] = useState({});
  const [operation, setOperation] = useState('');

  const updateCell = useCallback((cellKey, value) => {
    setCellData(prev => ({
      ...prev,
      [cellKey]: value
    }));
  }, []);

  const executeOperation = useCallback(() => {
    if (!operation.trim()) return;

    try {
      const results = executeFormula(operation.toUpperCase(), cellData);
      
      // Update cells with results
      setCellData(prev => ({
        ...prev,
        ...results
      }));

      // Show success message
      alert(`Operation ${operation} executed successfully!`);
    } catch (error) {
      alert(`Error executing operation: ${error.message}`);
    }
  }, [operation, cellData]);

  const clearAll = useCallback(() => {
    setCellData({});
    setOperation('');
  }, []);

  const clearColumn = useCallback((col) => {
    const colLetter = String.fromCharCode(65 + col);
    setCellData(prev => {
      const newData = { ...prev };
      Object.keys(newData).forEach(key => {
        if (key.startsWith(colLetter)) {
          delete newData[key];
        }
      });
      return newData;
    });
  }, []);

  const clearRow = useCallback((row) => {
    const rowNum = row + 1;
    setCellData(prev => {
      const newData = { ...prev };
      Object.keys(newData).forEach(key => {
        if (key.endsWith(rowNum.toString())) {
          delete newData[key];
        }
      });
      return newData;
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>🧮 Hisab Calculator</h1>
        <p>Excel-like desktop calculator with spreadsheet functionality</p>
      </header>
      
      <OperationBar
        operation={operation}
        setOperation={setOperation}
        executeOperation={executeOperation}
        clearAll={clearAll}
      />
      
      <SpreadsheetGrid
        cellData={cellData}
        updateCell={updateCell}
        clearColumn={clearColumn}
        clearRow={clearRow}
      />
    </div>
  );
}

export default App;