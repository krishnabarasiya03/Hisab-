const { app, BrowserWindow, Menu, shell } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');

let mainWindow;

// Error handling for unhandled exceptions
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  // Don't exit in production, just log the error
  if (isDev) {
    process.exit(1);
  }
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  // Don't exit in production, just log the error
});

function createWindow() {
  // Create the browser window
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 700,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js')
    },
    // Conditionally set icon only if it exists to prevent startup errors
    ...((() => {
      const fs = require('fs');
      const iconPath = process.platform === 'win32' 
        ? path.join(__dirname, 'assets/icon.ico')
        : process.platform === 'darwin'
        ? path.join(__dirname, 'assets/icon.icns')
        : path.join(__dirname, 'assets/icon.png');
      
      return fs.existsSync(iconPath) ? { icon: iconPath } : {};
    })()),
    title: 'Hisab Calculator',
    show: false, // Don't show until ready
    webSecurity: true
  });

  // Load the app
  const startUrl = isDev 
    ? 'http://localhost:3000' 
    : `file://${path.join(__dirname, 'build/index.html')}`;
  
  mainWindow.loadURL(startUrl).catch((error) => {
    console.error('Failed to load URL:', error);
    // Try loading a fallback error page or show error dialog
    const { dialog } = require('electron');
    dialog.showErrorBox(
      'Loading Error', 
      `Failed to load the application.\n\nError: ${error.message}\n\nPlease check that the app was built correctly by running: npm run build`
    );
  });

  // Show window when ready to prevent white screen flash
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    
    // Open DevTools in development
    if (isDev) {
      mainWindow.webContents.openDevTools();
    }
  });

  // Handle window closed
  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Create application menu
  createMenu();
}

function createMenu() {
  const template = [
    {
      label: 'File',
      submenu: [
        {
          label: 'New',
          accelerator: 'CmdOrCtrl+N',
          click: () => {
            mainWindow.webContents.send('clear-all');
          }
        },
        { type: 'separator' },
        {
          label: 'Exit',
          accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
          click: () => {
            app.quit();
          }
        }
      ]
    },
    {
      label: 'Edit',
      submenu: [
        { role: 'undo' },
        { role: 'redo' },
        { type: 'separator' },
        { role: 'cut' },
        { role: 'copy' },
        { role: 'paste' }
      ]
    },
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
        { type: 'separator' },
        { role: 'togglefullscreen' }
      ]
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'About Hisab Calculator',
          click: () => {
            require('electron').dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'About Hisab Calculator',
              message: 'Hisab Calculator v1.0.0',
              detail: 'Excel-like desktop calculator with spreadsheet functionality\n\nBuilt with Electron and React'
            });
          }
        },
        {
          label: 'GitHub Repository',
          click: () => {
            shell.openExternal('https://github.com/krishnabarasiya03/Hisab-');
          }
        }
      ]
    }
  ];

  // macOS specific menu adjustments
  if (process.platform === 'darwin') {
    template.unshift({
      label: app.getName(),
      submenu: [
        { role: 'about' },
        { type: 'separator' },
        { role: 'services' },
        { type: 'separator' },
        { role: 'hide' },
        { role: 'hideothers' },
        { role: 'unhide' },
        { type: 'separator' },
        { role: 'quit' }
      ]
    });
  }

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

// App event handlers
app.whenReady().then(() => {
  createWindow();
  
  // Set app user model ID for Windows notifications
  if (process.platform === 'win32') {
    app.setAppUserModelId('com.krishnabarasiya.hisab');
  }
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// Handle protocol for Windows deep linking
if (process.platform === 'win32') {
  app.setAsDefaultProtocolClient('hisab');
}

// Improve app quit behavior on Windows
app.on('before-quit', (event) => {
  // Allow graceful shutdown
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.close();
  }
});

// Security: Prevent new window creation and handle external links safely
app.on('web-contents-created', (event, contents) => {
  contents.setWindowOpenHandler(({ url }) => {
    // Open external links in default browser
    shell.openExternal(url);
    return { action: 'deny' };
  });
  
  // Prevent navigation to external URLs
  contents.on('will-navigate', (event, url) => {
    if (url !== contents.getURL()) {
      event.preventDefault();
      shell.openExternal(url);
    }
  });
});