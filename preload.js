const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // Add any needed APIs here for communication with main process
  clearAll: () => ipcRenderer.invoke('clear-all'),
  
  // Platform detection for conditional behavior
  platform: process.platform,
  
  // Version info
  versions: {
    node: process.versions.node,
    chrome: process.versions.chrome,
    electron: process.versions.electron
  }
});

// Listen for commands from main process
ipcRenderer.on('clear-all', () => {
  // Send clear command to React app
  window.dispatchEvent(new CustomEvent('clear-all'));
});