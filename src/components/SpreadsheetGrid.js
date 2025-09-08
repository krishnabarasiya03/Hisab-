import React, { useState, useCallback, useEffect, useRef } from 'react';
import ContextMenu from './ContextMenu';
import { performColumnOperation, performRowOperation } from '../utils/operations';

const SpreadsheetGrid = ({ cellData, updateCell, clearColumn, clearRow }) => {
  const [contextMenu, setContextMenu] = useState(null);
  const [selectedCell, setSelectedCell] = useState({ row: 0, col: 0 });
  const cellRefs = useRef({});
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

  // Helper function to get cell key from row/col
  const getCellKey = useCallback((row, col) => {
    return `${String.fromCharCode(65 + col)}${row + 1}`;
  }, []);

  // Helper function to move selection and focus
  const moveSelection = useCallback((newRow, newCol) => {
    // Boundary checking
    if (newRow < 0 || newRow >= ROWS || newCol < 0 || newCol >= COLS) {
      return;
    }
    
    setSelectedCell({ row: newRow, col: newCol });
    
    // Focus the new cell
    const cellKey = getCellKey(newRow, newCol);
    const cellRef = cellRefs.current[cellKey];
    if (cellRef) {
      cellRef.focus();
    }
  }, [getCellKey]);

  // Handle keyboard navigation
  const handleKeyDown = useCallback((e) => {
    const { row, col } = selectedCell;
    
    switch (e.key) {
      case 'ArrowUp':
        e.preventDefault();
        moveSelection(row - 1, col);
        break;
      case 'ArrowDown':
        e.preventDefault();
        moveSelection(row + 1, col);
        break;
      case 'ArrowLeft':
        e.preventDefault();
        moveSelection(row, col - 1);
        break;
      case 'ArrowRight':
        e.preventDefault();
        moveSelection(row, col + 1);
        break;
      case 'Tab':
        e.preventDefault();
        // Tab moves right, then down to next row
        if (col < COLS - 1) {
          moveSelection(row, col + 1);
        } else if (row < ROWS - 1) {
          moveSelection(row + 1, 0);
        }
        break;
      case 'Enter':
        e.preventDefault();
        // Enter moves down
        moveSelection(row + 1, col);
        break;
      default:
        break;
    }
  }, [selectedCell, moveSelection]);

  // Add keyboard event listener
  useEffect(() => {
    const handleGlobalKeyDown = (e) => {
      // Only handle navigation if focus is on a cell input
      if (e.target && e.target.tagName === 'INPUT' && e.target.closest('.grid-cell')) {
        handleKeyDown(e);
      }
    };

    document.addEventListener('keydown', handleGlobalKeyDown);
    return () => {
      document.removeEventListener('keydown', handleGlobalKeyDown);
    };
  }, [handleKeyDown]);

  // Handle cell click to update selected cell
  const handleCellClick = useCallback((row, col) => {
    setSelectedCell({ row, col });
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
      const isSelected = selectedCell.row === row && selectedCell.col === col;
      cells.push(
        <div key={cellKey} className={`grid-cell ${isSelected ? 'selected' : ''}`}>
          <input
            ref={(el) => {
              if (el) {
                cellRefs.current[cellKey] = el;
              }
            }}
            type="text"
            value={getCellValue(cellKey)}
            onChange={(e) => handleCellChange(cellKey, e.target.value)}
            onClick={() => handleCellClick(row, col)}
            onFocus={() => handleCellClick(row, col)}
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