# SAP MCP Server - Setup Instructions

## Quick Setup on New Machine

### Prerequisites
- **Python 3.7+** (for Python implementation)
- **Node.js 18.0+** (for TypeScript implementation)
- **VS Code** or **Claude Desktop** (for MCP integration)

## Step 1: Clone and Setup Project

```bash
# Clone the repository
git clone https://github.com/USERNAME/mcp-sap-gui-advanced.git
cd mcp-sap-gui-advanced
```

## Option 1: Python Implementation (Recommended)

### 1. Setup Python Environment
```bash
# Navigate to python folder
cd python

# No dependencies needed - uses Python standard library only!
# Test immediately:
python test_comprehensive.py
```

### 2. Configure Claude Desktop
```bash
# Copy the configuration template
# Windows
copy claude_desktop_direct.json "%APPDATA%\Claude\claude_desktop_config.json"

# macOS/Linux  
cp claude_desktop_direct.json ~/.config/claude/claude_desktop_config.json
```

**IMPORTANT**: Edit the copied configuration file and replace `REPLACE_WITH_FULL_PATH_TO_PROJECT` with your actual project path:

**Windows Example:**
```json
{
  "mcpServers": {
    "sap-automation": {
      "command": "python",
      "args": ["C:/Users/USERNAME/mcp-sap-gui-advanced/python/direct_sap_server.py"],
      "cwd": "C:/Users/USERNAME/mcp-sap-gui-advanced/python"
    }
  }
}
```

**macOS/Linux Example:**
```json
{
  "mcpServers": {
    "sap-automation": {
      "command": "python",
      "args": ["/home/username/mcp-sap-gui-advanced/python/direct_sap_server.py"],
      "cwd": "/home/username/mcp-sap-gui-advanced/python"
    }
  }
}
```

## Option 2: TypeScript Implementation

### 1. Install Dependencies
```bash
# Navigate to typescript folder
cd typescript

# Install Node.js dependencies
npm install

# Build the project
npm run build
```

### 2. Test Setup
```bash
npm test
# OR
node test-comprehensive.js
```

### 3. Configure Claude Desktop
```bash
# Copy the configuration template
# Windows
copy claude-desktop-config.json "%APPDATA%\Claude\claude_desktop_config.json"

# macOS/Linux
cp claude-desktop-config.json ~/.config/claude/claude_desktop_config.json
```

**IMPORTANT**: Edit the copied configuration file and replace `REPLACE_WITH_FULL_PATH_TO_PROJECT` with your actual project path:

**Windows Example:**
```json
{
  "mcpServers": {
    "sap-automation-typescript": {
      "command": "node",
      "args": ["C:/Users/USERNAME/mcp-sap-gui-advanced/typescript/direct-sap-server.js"],
      "cwd": "C:/Users/USERNAME/mcp-sap-gui-advanced/typescript"
    }
  }
}
```

**macOS/Linux Example:**
```json
{
  "mcpServers": {
    "sap-automation-typescript": {
      "command": "node",
      "args": ["/home/username/mcp-sap-gui-advanced/typescript/direct-sap-server.js"],
      "cwd": "/home/username/mcp-sap-gui-advanced/typescript"
    }
  }
}
```

## Verification

After setup, restart Claude Desktop and verify:
1. **22 SAP automation tools** appear in Claude Desktop
2. You can ask: "List all available SAP automation tools"
3. Expected response: Complete list of connection, navigation, field operations, etc.

## Troubleshooting

### Python Issues
- Ensure Python 3.7+ is installed: `python --version`
- Test basic functionality: `python test_direct.py`

### TypeScript Issues  
- Ensure Node.js 18+ is installed: `node --version`
- Reinstall dependencies: `npm install`
- Rebuild project: `npm run build`

### Claude Desktop Integration
- Restart Claude Desktop after configuration
- Check configuration file syntax (JSON format)
- Verify file paths are absolute in configuration

## File Structure After Setup

```
SAP MCP Server/
├── python/
│   ├── direct_sap_server.py          # Main server (22 tools)
│   ├── requirements.txt              # Dependencies (none needed)
│   ├── claude_desktop_direct.json    # Claude config
│   └── test_comprehensive.py         # Test suite
├── typescript/
│   ├── direct-sap-server.ts          # Main server source
│   ├── direct-sap-server.js          # Compiled server
│   ├── package.json                  # Dependencies
│   ├── claude-desktop-config.json    # Claude config
│   └── test-comprehensive.js         # Test suite
└── SETUP.md                          # This file
```

## Production Deployment

### Python (Minimal Setup)
- Copy `direct_sap_server.py` and `claude_desktop_direct.json`
- No additional dependencies required
- Works with any Python 3.7+ installation

### TypeScript (Development Setup)
- Copy entire `typescript/` folder
- Run `npm install` and `npm run build`
- Requires Node.js runtime environment

Choose Python for **simplicity** or TypeScript for **development features**.
