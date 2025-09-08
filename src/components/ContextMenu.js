import React, { useEffect, useRef } from 'react';

const ContextMenu = ({ x, y, label, onAction, onClose }) => {
  const menuRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        onClose();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [onClose]);

  const menuItems = [
    { action: 'sum', label: `Sum ${label}` },
    { action: 'multiply', label: `Multiply ${label}` },
    { action: 'add', label: `Add to ${label}` },
    { action: 'subtract', label: `Subtract from ${label}` },
    { action: 'divide', label: `Divide ${label}` },
    'separator',
    { action: 'clear', label: `Clear ${label}` }
  ];

  return (
    <div
      ref={menuRef}
      className="context-menu"
      style={{ left: x, top: y }}
    >
      {menuItems.map((item, index) => {
        if (item === 'separator') {
          return <div key={index} className="context-menu-separator" />;
        }
        
        return (
          <div
            key={index}
            className="context-menu-item"
            onClick={() => onAction(item.action)}
          >
            {item.label}
          </div>
        );
      })}
    </div>
  );
};

export default ContextMenu;