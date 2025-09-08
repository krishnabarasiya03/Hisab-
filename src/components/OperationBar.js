import React from 'react';

const OperationBar = ({ operation, setOperation, executeOperation, clearAll }) => {
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      executeOperation();
    }
  };

  return (
    <div className="operation-bar">
      <label htmlFor="operation-input">Operation:</label>
      <input
        id="operation-input"
        type="text"
        value={operation}
        onChange={(e) => setOperation(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Enter formula like A*B, C+D, etc."
      />
      <button 
        className="btn-execute"
        onClick={executeOperation}
      >
        Execute
      </button>
      <button 
        className="btn-clear"
        onClick={clearAll}
      >
        Clear All
      </button>
    </div>
  );
};

export default OperationBar;