# SAP MCP Server - Comprehensive SAP GUI Automation

A Model Context Protocol (MCP) server providing comprehensive SAP GUI automation capabilities for Claude Desktop integration. Features 22 professional SAP automation tools implemented in both Python and TypeScript.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Clone the repository
git clone https://github.com/USERNAME/mcp-sap-gui-advanced.git
cd mcp-sap-gui-advanced

# Run the quick setup script
# Windows:
quick-setup.bat

# macOS/Linux:
chmod +x quick-setup.sh
./quick-setup.sh
```

### Option 2: Manual Setup
See [SETUP.md](SETUP.md) for detailed manual installation instructions.

## 🔒 Privacy & Security
This project operates entirely locally and does not collect or transmit personal information. See [PRIVACY.md](PRIVACY.md) for complete details.

## Project Structure

```
SAP MCP Server/
├── python/                 # Python implementation
│   ├── direct_sap_server.py     # 22 SAP automation tools
│   ├── test_comprehensive.py    # Full test suite
│   └── claude_desktop_direct.json
├── typescript/             # TypeScript implementation
│   ├── direct-sap-server.ts     # 22 SAP automation tools
│   ├── test-comprehensive.js    # Full test suite
│   └── claude-desktop-config.json
└── README.md              # This file
```

## Comprehensive SAP Automation (22 Tools)

### Connection & Session Management
- **sap_connect** - Connect to SAP systems with credentials
- **sap_disconnect** - Disconnect from SAP systems
- **sap_get_sessions** - Manage multiple SAP sessions

### Navigation & Transaction Management
- **sap_navigate** - Navigate to transactions (VA01, MM01, SE80, etc.)
- **sap_navigate_back** - Navigate back (F3 equivalent)
- **sap_navigate_exit** - Exit transactions (F15 equivalent)

### Field Operations
- **sap_input_field** - Input data into SAP fields
- **sap_get_field_value** - Retrieve field values
- **sap_clear_field** - Clear field contents

### Button & Menu Operations
- **sap_press_button** - Press GUI buttons
- **sap_select_menu** - Access menu functions

### Function Key Operations
- **sap_send_key** - Send function keys (F1-F24, Enter, Escape)

### Table Operations
- **sap_get_table_data** - Extract table/grid data
- **sap_set_table_cell** - Modify table cells
- **sap_select_table_row** - Select table rows

### Screen Information
- **sap_get_screen_info** - Get current screen details
- **sap_get_status_message** - Read status messages

### Visual Operations
- **sap_screenshot** - Capture screen images

### Advanced Operations
- **sap_execute_transaction** - Multi-step transaction processing
- **sap_wait_for_screen** - Screen loading synchronization

### Data Exchange
- **sap_export_data** - Export to CSV, Excel formats
- **sap_import_data** - Import data from files

## 🛠️ **Quick Start**

### TypeScript Version
```bash
cd typescript
npm install
npm run build
npm start
```

### Python Version
```bash
cd python
uv install
uv run python -m sap_mcp_server.main
```

## 🔧 **MCP Client Configuration**

Both implementations work with any MCP client:

### Claude Desktop (`claude_desktop_config.json`)

**TypeScript:**
```json
{
  "mcpServers": {
    "sap-automation-ts": {
      "command": "node",
      "args": ["./typescript/build/index.js"],
      "cwd": "/path/to/sap-mcp-server"
    }
  }
}
```

**Python:**
```json
{
  "mcpServers": {
    "sap-automation-py": {
      "command": "python",
      "args": ["-m", "sap_mcp_server.main"],
      "cwd": "/path/to/sap-mcp-server/python"
    }
  }
}
```

##  **Requirements**

### Common Requirements
- **SAP GUI** installed (for actual SAP automation)
- **Windows** (recommended for SAP GUI Scripting)
- **MCP-compatible client** (Claude Desktop, VS Code, etc.)

### TypeScript Specific
- **Node.js 17+**
- **npm** or **yarn**

### Python Specific  
- **Python 3.10+**
- **uv** (recommended) or **pip**

##  **Example Usage**

Both implementations support identical natural language commands:

### Connect to SAP
```
"Connect me to SAP system DEV with client 100, username john.doe, password mypass123, server sap-dev.company.com"
```

### Navigate and Input Data
```
"Navigate to transaction VA01 and create a sales order with customer 12345 and material ABC123"
```

### Extract Data
```
"Extract customer data from the current screen, specifically the name, address, and contact fields"
```

##  **Security & Integration**

Both implementations include:
- **Placeholder functions** ready for your SAP driver integration
- **Secure credential handling** with environment variables
- **Input validation** with schema enforcement
- **Error handling** and logging
- **Documentation** and examples

##  **Migration Between Languages**

The **MCP protocol is language-agnostic**, so you can:
- Start with one implementation and switch later
- Run both simultaneously for different use cases
- Choose based on your team's expertise
- Integrate with any existing SAP automation code

##  **Documentation**

- **[TypeScript README](./typescript/README.md)** - TypeScript-specific setup and usage
- **[Python README](./python/README.md)** - Python-specific setup and usage  
- **[Integration Guide](./INTEGRATION_GUIDE.md)** - How to integrate with your SAP driver
- **[MCP Documentation](https://modelcontextprotocol.io)** - Official MCP protocol docs

##  **Debugging**

Use the [MCP Inspector](https://github.com/modelcontextprotocol/inspector) with either implementation:

**Python:**
```bash
python test_comprehensive.py
```

**TypeScript:**
```bash
node test-comprehensive.js
```

## License

This project is licensed under the MIT License.
