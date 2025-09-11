@echo off
REM SAP MCP Server - Automated Setup Script for Windows
REM This script sets up the SAP MCP Server on a new Windows machine

echo 🚀 SAP MCP Server Setup Script
echo ==============================

REM Check if we're in the right directory
if not exist "README.md" (
    echo ❌ Error: Please run this script from the SAP MCP Server root directory
    pause
    exit /b 1
)

echo 📋 Choose implementation:
echo 1) Python (Recommended - No dependencies)
echo 2) TypeScript (Advanced - Requires Node.js)
echo 3) Both implementations
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" goto :python
if "%choice%"=="2" goto :typescript  
if "%choice%"=="3" goto :both
echo ❌ Invalid choice
pause
exit /b 1

:python
:both
echo.
echo 🐍 Setting up Python implementation...
cd python

REM Check Python version
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python not found. Please install Python 3.7+
    pause
    exit /b 1
)

echo ✅ Python found
for /f "tokens=*" %%i in ('python --version') do echo %%i

REM Test the server
echo 🧪 Testing Python server...
python test_comprehensive.py
if %errorlevel% neq 0 (
    echo ❌ Python server test failed
    pause
    exit /b 1
)
echo ✅ Python server test passed!

cd ..
if "%choice%"=="1" goto :complete

:typescript
echo.
echo 📦 Setting up TypeScript implementation...
cd typescript

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)

echo ✅ Node.js found
for /f "tokens=*" %%i in ('node --version') do echo %%i

REM Install dependencies
echo 📦 Installing dependencies...
npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed successfully

REM Build project
echo 🔨 Building TypeScript project...
npm run build
if %errorlevel% neq 0 (
    echo ❌ TypeScript build failed
    pause
    exit /b 1
)
echo ✅ TypeScript build successful

REM Test the server
echo 🧪 Testing TypeScript server...
node test-comprehensive.js
if %errorlevel% neq 0 (
    echo ❌ TypeScript server test failed
    pause
    exit /b 1
)
echo ✅ TypeScript server test passed!

cd ..

:complete
echo.
echo 🎉 Setup completed successfully!
echo.
echo 📋 Next steps:
echo 1. Copy the appropriate claude-desktop configuration:

if "%choice%"=="1" (
    echo    Python: copy python\claude_desktop_direct.json "%%APPDATA%%\Claude\claude_desktop_config.json"
) else if "%choice%"=="2" (
    echo    TypeScript: copy typescript\claude-desktop-config.json "%%APPDATA%%\Claude\claude_desktop_config.json"
) else (
    echo    Python: copy python\claude_desktop_direct.json "%%APPDATA%%\Claude\claude_desktop_config.json"
    echo    TypeScript: copy typescript\claude-desktop-config.json "%%APPDATA%%\Claude\claude_desktop_config.json"
)

echo 2. Restart Claude Desktop
echo 3. Ask Claude: 'List all available SAP automation tools'
echo.
echo ✅ Your SAP MCP Server with 22 automation tools is ready!
echo.
pause
