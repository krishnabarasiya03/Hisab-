import React, { useState, useCallback } from 'react';
import ContextMenu from './ContextMenu';
import { performColumnOperation, performRowOperation } from '../utils/operations';

const SpreadsheetGrid = ({ cellData, updateCell, clearColumn, clearRow }) => {
  const [contextMenu, setContextMenu] = useState(null);
  const ROWS = 20;
  const COLS = 10;

  const getCellValue = useCallback((cellKey) => {
    const value = cellData[cellKey];
    if (value === null || value === undefined) return '';
    return value.toString();
  }, [cellData]);

  const handleCellChange = useCallback((cellKey, value) => {
    // Try to convert to number if possible
    let processedValue = value;
    if (value && !isNaN(value) && !isNaN(parseFloat(value))) {
      processedValue = value.includes('.') ? parseFloat(value) : parseInt(value);
    }
    updateCell(cellKey, processedValue);
  }, [updateCell]);

  const handleColumnRightClick = useCallback((e, col) => {
    e.preventDefault();
    const colLetter = String.fromCharCode(65 + col);
    setContextMenu({
      x: e.clientX,
      y: e.clientY,
      type: 'column',
      index: col,
      label: `Column ${colLetter}`
    });
  }, []);

  const handleRowRightClick = useCallback((e, row) => {
    e.preventDefault();
    const rowNum = row + 1;
    setContextMenu({
      x: e.clientX,
      y: e.clientY,
      type: 'row',
      index: row,
      label: `Row ${rowNum}`
    });
  }, []);

  const handleContextMenuAction = useCallback((action) => {
    if (!contextMenu) return;

    const { type, index } = contextMenu;
    
    if (type === 'column') {
      if (action === 'clear') {
        clearColumn(index);
      } else {
        const value = action === 'sum' ? null : prompt(`Enter value to ${action}:`);
        if (action === 'sum' || (value !== null && !isNaN(value))) {
          const results = performColumnOperation(
            index, 
            action, 
            value ? parseFloat(value) : null, 
            cellData,
            ROWS
          );
          
          // Update cells with results
          Object.entries(results.updates).forEach(([key, val]) => {
            updateCell(key, val);
          });
          
          if (results.message) {
            alert(results.message);
          }
        }
      }
    } else if (type === 'row') {
      if (action === 'clear') {
        clearRow(index);
      } else {
        const value = action === 'sum' ? null : prompt(`Enter value to ${action}:`);
        if (action === 'sum' || (value !== null && !isNaN(value))) {
          const results = performRowOperation(
            index, 
            action, 
            value ? parseFloat(value) : null, 
            cellData,
            COLS
          );
          
          // Update cells with results
          Object.entries(results.updates).forEach(([key, val]) => {
            updateCell(key, val);
          });
          
          if (results.message) {
            alert(results.message);
          }
        }
      }
    }
    
    setContextMenu(null);
  }, [contextMenu, clearColumn, clearRow, cellData, updateCell]);

  const closeContextMenu = useCallback(() => {
    setContextMenu(null);
  }, []);

  // Generate grid rows
  const gridRows = [];
  
  // Header row
  const headerRow = (
    <div key="header" className="grid-row">
      <div className="grid-header row-header"></div>
      {Array.from({ length: COLS }, (_, col) => (
        <div
          key={`header-${col}`}
          className="grid-header"
          onContextMenu={(e) => handleColumnRightClick(e, col)}
        >
          {String.fromCharCode(65 + col)}
        </div>
      ))}
    </div>
  );
  gridRows.push(headerRow);

  // Data rows
  for (let row = 0; row < ROWS; row++) {
    const cells = [];
    
    // Row header
    cells.push(
      <div
        key={`row-header-${row}`}
        className="grid-header row-header"
        onContextMenu={(e) => handleRowRightClick(e, row)}
      >
        {row + 1}
      </div>
    );
    
    // Data cells
    for (let col = 0; col < COLS; col++) {
      const cellKey = `${String.fromCharCode(65 + col)}${row + 1}`;
      cells.push(
        <div key={cellKey} className="grid-cell">
          <input
            type="text"
            value={getCellValue(cellKey)}
            onChange={(e) => handleCellChange(cellKey, e.target.value)}
          />
        </div>
      );
    }
    
    gridRows.push(
      <div key={`row-${row}`} className="grid-row">
        {cells}
      </div>
    );
  }

  return (
    <div className="spreadsheet-container" onClick={closeContextMenu}>
      <div className="spreadsheet-grid">
        {gridRows}
      </div>
      
      {contextMenu && (
        <ContextMenu
          x={contextMenu.x}
          y={contextMenu.y}
          label={contextMenu.label}
          onAction={handleContextMenuAction}
          onClose={closeContextMenu}
        />
      )}
    </div>
  );
};

export default SpreadsheetGrid;