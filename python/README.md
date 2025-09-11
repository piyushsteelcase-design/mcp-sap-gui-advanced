# SAP MCP Server - Python Implementation

This directory contains the Python implementation of the SAP MCP (Model Context Protocol) server with comprehensive SAP GUI automation capabilities using direct JSON-RPC protocol implementation.

## Files

- `direct_sap_server.py` - Main MCP server with 22 SAP automation tools
- `test_direct.py` - Basic connectivity test
- `test_comprehensive.py` - Full SAP tools test suite
- `claude_desktop_direct.json` - Claude Desktop configuration
- `pyproject.toml` - Python project configuration

## SAP Automation Capabilities

### 22 Professional SAP Tools Available:

**Connection & Session Management:**
- `sap_connect` - Connect to SAP system with credentials
- `sap_disconnect` - Disconnect from SAP system
- `sap_get_sessions` - Get list of active SAP sessions

**Navigation & Transaction Management:**
- `sap_navigate` - Navigate to SAP transaction (VA01, MM01, SE80, etc.)
- `sap_navigate_back` - Navigate back (F3 equivalent)
- `sap_navigate_exit` - Exit current transaction (F15 equivalent)

**Field Operations:**
- `sap_input_field` - Input data into specific SAP fields
- `sap_get_field_value` - Get value from SAP fields
- `sap_clear_field` - Clear specific SAP fields

**Button & Menu Operations:**
- `sap_press_button` - Press buttons in SAP GUI
- `sap_select_menu` - Select menu items

**Function Key Operations:**
- `sap_send_key` - Send function keys (F1-F24, Enter, Escape, etc.)

**Table Operations:**
- `sap_get_table_data` - Extract data from SAP tables/grids
- `sap_set_table_cell` - Set values in table cells
- `sap_select_table_row` - Select rows in SAP tables

**Screen Information:**
- `sap_get_screen_info` - Get current screen information
- `sap_get_status_message` - Get status bar messages

**Visual Operations:**
- `sap_screenshot` - Take screenshots of SAP screens

**Advanced Operations:**
- `sap_execute_transaction` - Execute multi-step transactions
- `sap_wait_for_screen` - Wait for specific screens to load

**Data Exchange:**
- `sap_export_data` - Export SAP data to files (CSV, Excel, etc.)
- `sap_import_data` - Import data into SAP from files

## Quick Start

1. No dependencies needed - uses only Python standard library

2. Test basic connectivity:
```bash
python test_direct.py
```

3. Test all SAP automation tools:
```bash
python test_comprehensive.py
```

4. Configure Claude Desktop:
```bash
copy claude_desktop_direct.json "C:\Users\%USERNAME%\AppData\Roaming\Claude\claude_desktop_config.json"
```

5. Restart Claude Desktop to activate SAP automation

## Features

- Direct MCP protocol implementation (no external libraries)
- Claude Desktop compatible
- 22 comprehensive SAP automation tools
- Professional SAP GUI workflow automation
- Session management and multi-system support
- Table data extraction and manipulation
- Advanced transaction processing
- Data import/export capabilities
- Screenshot and visual operations
- Complete error handling and logging

## Usage Examples

**Create Sales Order:**
Ask Claude Desktop: "Connect to SAP DEV system and create a sales order in VA01 for customer 1000"

**Extract Data:**
Ask Claude Desktop: "Navigate to ME03 and extract all line items from purchase order 4500000001"

**Process Multiple Records:**
Ask Claude Desktop: "Execute transaction XD02 to update customer master data from a CSV file"

## Real SAP GUI Integration

When SAP GUI is available, the server can be enhanced to use actual SAP COM APIs instead of simulation. The architecture is designed for easy integration with real SAP systems.

## Testing

Run the comprehensive test to verify all 22 tools:
```bash
python test_comprehensive.py
```

Expected output: "SUCCESS: All 22 SAP automation tools are working!"
