@echo off
REM Quick Setup Script for SAP MCP Server (Windows)
REM This script helps users configure the MCP server after cloning

echo 🚀 SAP MCP Server - Quick Setup
echo ================================

REM Get the current directory
set "CURRENT_DIR=%CD%"
echo 📁 Project directory: %CURRENT_DIR%

REM Set config directory for Windows
set "CONFIG_DIR=%APPDATA%\Claude"
echo 🖥️  Detected OS: Windows

REM Choose implementation
echo.
echo Choose implementation:
echo 1) Python (Recommended - no dependencies)
echo 2) TypeScript (requires Node.js)
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" (
    echo 🐍 Setting up Python implementation...
    set "IMPL_DIR=%CURRENT_DIR%\python"
    set "SERVER_FILE=direct_sap_server.py"
    set "COMMAND=python"
    
    REM Test Python
    cd python
    echo 🧪 Testing Python server...
    python test_direct.py
    cd ..
) else if "%choice%"=="2" (
    echo 📦 Setting up TypeScript implementation...
    set "IMPL_DIR=%CURRENT_DIR%\typescript"
    set "SERVER_FILE=direct-sap-server.js"
    set "COMMAND=node"
    
    REM Install dependencies and build
    cd typescript
    echo 📦 Installing dependencies...
    npm install
    echo 🔨 Building project...
    npm run build
    echo 🧪 Testing TypeScript server...
    npm test
    cd ..
) else (
    echo ❌ Invalid choice. Exiting.
    exit /b 1
)

REM Create Claude config directory if it doesn't exist
if not exist "%CONFIG_DIR%" mkdir "%CONFIG_DIR%"

REM Generate the correct configuration
echo ⚙️  Generating Claude Desktop configuration...

(
echo {
echo   "mcpServers": {
echo     "sap-automation": {
echo       "command": "%COMMAND%",
echo       "args": ["%IMPL_DIR:\=/%/%SERVER_FILE%"],
echo       "cwd": "%IMPL_DIR:\=/%"
echo     }
echo   }
echo }
) > "%CONFIG_DIR%\claude_desktop_config.json"

echo ✅ Configuration created at: %CONFIG_DIR%\claude_desktop_config.json
echo.
echo 🎉 Setup Complete!
echo.
echo Next steps:
echo 1. Restart Claude Desktop
echo 2. Ask Claude: 'List all available SAP automation tools'
echo 3. You should see 22 SAP automation tools available
echo.
echo 📖 For manual setup instructions, see SETUP.md
pause
