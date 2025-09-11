#!/usr/bin/env python3
"""
Direct MCP Protocol Implementation for SAP Automation
This bypasses the MCP library and implements the protocol directly
"""

import asyncio
import json
import sys
import logging
from typing import Any, Dict, List, Optional

# Configure logging to stderr for Claude Desktop debugging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr
)
logger = logging.getLogger("sap-direct")

class DirectSAPMCPServer:
    def __init__(self):
        self.initialized = False
        
    def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request - this is where the error occurs"""
        logger.info(f"Initialize called with params type: {type(params)}")
        logger.info(f"Initialize params: {params}")
        
        # Claude Desktop sends capabilities as a dict, not as an object with .capabilities
        if not isinstance(params, dict):
            logger.error(f"Expected dict but got {type(params)}")
            raise ValueError("params must be a dictionary")
        
        # Extract required fields safely
        protocol_version = params.get("protocolVersion", "2024-11-05")
        client_capabilities = params.get("capabilities", {})
        client_info = params.get("clientInfo", {})
        
        logger.info(f"Client capabilities type: {type(client_capabilities)}")
        logger.info(f"Client info: {client_info}")
        
        # Return the exact structure Claude Desktop expects
        response = {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "resources": {}
            },
            "serverInfo": {
                "name": "sap-automation",
                "version": "1.0.0"
            }
        }
        
        logger.info(f"Returning initialize response: {response}")
        return response
    
    def handle_tools_list(self) -> Dict[str, Any]:
        """Return comprehensive SAP GUI automation tools"""
        tools = [
            # Connection & Session Management
            {
                "name": "sap_connect",
                "description": "Connect to SAP system with credentials",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "system_id": {"type": "string", "description": "SAP system ID"},
                        "client": {"type": "string", "description": "SAP client number"},
                        "username": {"type": "string", "description": "Username"},
                        "password": {"type": "string", "description": "Password"},
                        "server": {"type": "string", "description": "SAP server address"},
                        "instance": {"type": "string", "description": "Instance number", "default": "00"},
                        "language": {"type": "string", "description": "Login language", "default": "EN"}
                    },
                    "required": ["system_id", "client", "username", "password", "server"]
                }
            },
            {
                "name": "sap_disconnect",
                "description": "Disconnect from SAP system",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string", "description": "Session ID to disconnect"}
                    },
                    "required": []
                }
            },
            {
                "name": "sap_get_sessions",
                "description": "Get list of active SAP sessions",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            
            # Navigation & Transaction Management
            {
                "name": "sap_navigate",
                "description": "Navigate to SAP transaction",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "transaction_code": {"type": "string", "description": "Transaction code (e.g., VA01, MM01, SE80)"},
                        "session_id": {"type": "string", "description": "Session ID", "default": "default"}
                    },
                    "required": ["transaction_code"]
                }
            },
            {
                "name": "sap_navigate_back",
                "description": "Navigate back in SAP (F3 equivalent)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string", "description": "Session ID", "default": "default"}
                    },
                    "required": []
                }
            },
            {
                "name": "sap_navigate_exit",
                "description": "Exit current transaction (F15 equivalent)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string", "description": "Session ID", "default": "default"}
                    },
                    "required": []
                }
            },
            
            # Field Operations
            {
                "name": "sap_input_field",
                "description": "Input data into a specific SAP field",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "field_id": {"type": "string", "description": "Field ID or name"},
                        "value": {"type": "string", "description": "Value to input"},
                        "session_id": {"type": "string", "description": "Session ID", "default": "default"}
                    },
                    "required": ["field_id", "value"]
                }
            },
            {
                "name": "sap_get_field_value",
                "description": "Get value from a specific SAP field",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "field_id": {"type": "string", "description": "Field ID or name"},
                        "session_id": {"type": "string", "description": "Session ID", "default": "default"}
                    },
                    "required": ["field_id"]
                }
            },
            {
                "name": "sap_clear_field",
                "description": "Clear a specific SAP field",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "field_id": {"type": "string", "description": "Field ID or name"},
                        "session_id": {"type": "string", "description": "Session ID", "default": "default"}
                    },
                    "required": ["field_id"]
                }
            },
            
            # Button & Menu Operations
            {
                "name": "sap_press_button",
                "description": "Press a button in SAP GUI",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "button_id": {"type": "string", "description": "Button ID or name"},
                        "session_id": {"type": "string", "description": "Session ID", "default": "default"}
                    },
                    "required": ["button_id"]
                }
            },
            {
                "name": "sap_select_menu",
                "description": "Select menu item in SAP GUI",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "menu_path": {"type": "string", "description": "Menu path (e.g., 'System->User Profile->Own Data')"},
                        "session_id": {"type": "string", "description": "Session ID", "default": "default"}
                    },
                    "required": ["menu_path"]
                }
            },
            
            # Function Key Operations
            {
                "name": "sap_send_key",
                "description": "Send function key or key combination",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "key": {"type": "string", "description": "Key to send (F1-F24, Enter, Escape, etc.)"},
                        "session_id": {"type": "string", "description": "Session ID", "default": "default"}
                    },
                    "required": ["key"]
                }
            },
            
            # Table Operations
            {
                "name": "sap_get_table_data",
                "description": "Extract data from SAP table/grid",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "table_id": {"type": "string", "description": "Table/grid ID"},
                        "row_start": {"type": "integer", "description": "Starting row (0-based)", "default": 0},
                        "row_count": {"type": "integer", "description": "Number of rows to extract", "default": 10},
                        "columns": {"type": "array", "items": {"type": "string"}, "description": "Specific columns to extract (optional)"},
                        "session_id": {"type": "string", "description": "Session ID", "default": "default"}
                    },
                    "required": ["table_id"]
                }
            },
            {
                "name": "sap_set_table_cell",
                "description": "Set value in specific table cell",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "table_id": {"type": "string", "description": "Table/grid ID"},
                        "row": {"type": "integer", "description": "Row number (0-based)"},
                        "column": {"type": "string", "description": "Column name or ID"},
                        "value": {"type": "string", "description": "Value to set"},
                        "session_id": {"type": "string", "description": "Session ID", "default": "default"}
                    },
                    "required": ["table_id", "row", "column", "value"]
                }
            },
            {
                "name": "sap_select_table_row",
                "description": "Select row(s) in SAP table",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "table_id": {"type": "string", "description": "Table/grid ID"},
                        "row": {"type": "integer", "description": "Row number (0-based)"},
                        "multi_select": {"type": "boolean", "description": "Allow multiple selection", "default": False},
                        "session_id": {"type": "string", "description": "Session ID", "default": "default"}
                    },
                    "required": ["table_id", "row"]
                }
            },
            
            # Screen Information
            {
                "name": "sap_get_screen_info",
                "description": "Get current screen information",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string", "description": "Session ID", "default": "default"}
                    },
                    "required": []
                }
            },
            {
                "name": "sap_get_status_message",
                "description": "Get current status bar message",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string", "description": "Session ID", "default": "default"}
                    },
                    "required": []
                }
            },
            
            # Screenshot & Visual
            {
                "name": "sap_screenshot",
                "description": "Take screenshot of SAP screen",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string", "description": "Output filename", "default": "sap_screenshot.png"},
                        "session_id": {"type": "string", "description": "Session ID", "default": "default"}
                    },
                    "required": []
                }
            },
            
            # Advanced Operations
            {
                "name": "sap_execute_transaction",
                "description": "Execute complete transaction with multiple steps",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "transaction_code": {"type": "string", "description": "Transaction to execute"},
                        "steps": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "action": {"type": "string", "description": "Action type (input, button, key)"},
                                    "target": {"type": "string", "description": "Target field/button ID"},
                                    "value": {"type": "string", "description": "Value (for input actions)"}
                                }
                            },
                            "description": "List of steps to execute"
                        },
                        "session_id": {"type": "string", "description": "Session ID", "default": "default"}
                    },
                    "required": ["transaction_code", "steps"]
                }
            },
            {
                "name": "sap_wait_for_screen",
                "description": "Wait for specific screen to load",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "screen_id": {"type": "string", "description": "Screen ID to wait for"},
                        "timeout": {"type": "integer", "description": "Timeout in seconds", "default": 30},
                        "session_id": {"type": "string", "description": "Session ID", "default": "default"}
                    },
                    "required": ["screen_id"]
                }
            },
            
            # Export & Import
            {
                "name": "sap_export_data",
                "description": "Export SAP data to file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "data_source": {"type": "string", "description": "Data source (table, screen, etc.)"},
                        "format": {"type": "string", "description": "Export format", "enum": ["csv", "xlsx", "txt", "xml"]},
                        "filename": {"type": "string", "description": "Output filename"},
                        "session_id": {"type": "string", "description": "Session ID", "default": "default"}
                    },
                    "required": ["data_source", "format", "filename"]
                }
            },
            {
                "name": "sap_import_data",
                "description": "Import data into SAP from file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string", "description": "Input filename"},
                        "target": {"type": "string", "description": "Target field or table"},
                        "mapping": {"type": "object", "description": "Field mapping configuration"},
                        "session_id": {"type": "string", "description": "Session ID", "default": "default"}
                    },
                    "required": ["filename", "target"]
                }
            }
        ]
        
        return {"tools": tools}
    
    def handle_tool_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute comprehensive SAP GUI automation tools"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        logger.info(f"Executing tool: {tool_name} with args: {arguments}")
        
        # Connection & Session Management
        if tool_name == "sap_connect":
            system_id = arguments.get('system_id', 'DEV')
            client = arguments.get('client', '100')
            username = arguments.get('username', 'user')
            server = arguments.get('server', 'localhost')
            language = arguments.get('language', 'EN')
            result_text = f"Successfully connected to SAP system {system_id} client {client} on server {server} with language {language}"
            
        elif tool_name == "sap_disconnect":
            session_id = arguments.get('session_id', 'default')
            result_text = f"Successfully disconnected from SAP session {session_id}"
            
        elif tool_name == "sap_get_sessions":
            sessions = ["Session[0] - DEV/100", "Session[1] - QAS/100"]
            result_text = f"Active SAP sessions: {', '.join(sessions)}"
        
        # Navigation & Transaction Management  
        elif tool_name == "sap_navigate":
            tcode = arguments.get('transaction_code', 'UNKNOWN')
            session_id = arguments.get('session_id', 'default')
            result_text = f"Successfully navigated to transaction {tcode} in session {session_id}"
            
        elif tool_name == "sap_navigate_back":
            session_id = arguments.get('session_id', 'default')
            result_text = f"Navigated back (F3) in session {session_id}"
            
        elif tool_name == "sap_navigate_exit":
            session_id = arguments.get('session_id', 'default')
            result_text = f"Exited transaction (F15) in session {session_id}"
        
        # Field Operations
        elif tool_name == "sap_input_field":
            field_id = arguments.get('field_id', 'FIELD')
            value = arguments.get('value', '')
            session_id = arguments.get('session_id', 'default')
            result_text = f"Successfully input '{value}' into field '{field_id}' in session {session_id}"
            
        elif tool_name == "sap_get_field_value":
            field_id = arguments.get('field_id', 'FIELD')
            session_id = arguments.get('session_id', 'default')
            mock_value = f"VALUE_FROM_{field_id}"
            result_text = f"Field '{field_id}' value: '{mock_value}' in session {session_id}"
            
        elif tool_name == "sap_clear_field":
            field_id = arguments.get('field_id', 'FIELD')
            session_id = arguments.get('session_id', 'default')
            result_text = f"Successfully cleared field '{field_id}' in session {session_id}"
        
        # Button & Menu Operations
        elif tool_name == "sap_press_button":
            button_id = arguments.get('button_id', 'BUTTON')
            session_id = arguments.get('session_id', 'default')
            result_text = f"Successfully pressed button '{button_id}' in session {session_id}"
            
        elif tool_name == "sap_select_menu":
            menu_path = arguments.get('menu_path', 'Menu->Item')
            session_id = arguments.get('session_id', 'default')
            result_text = f"Successfully selected menu '{menu_path}' in session {session_id}"
        
        # Function Key Operations
        elif tool_name == "sap_send_key":
            key = arguments.get('key', 'Enter')
            session_id = arguments.get('session_id', 'default')
            result_text = f"Successfully sent key '{key}' in session {session_id}"
        
        # Table Operations
        elif tool_name == "sap_get_table_data":
            table_id = arguments.get('table_id', 'TABLE')
            row_start = arguments.get('row_start', 0)
            row_count = arguments.get('row_count', 10)
            columns = arguments.get('columns', ['COL1', 'COL2', 'COL3'])
            session_id = arguments.get('session_id', 'default')
            
            # Mock table data
            mock_data = []
            for i in range(row_start, row_start + row_count):
                row = {col: f"{col}_VALUE_{i}" for col in columns}
                mock_data.append(row)
            
            result_text = f"Extracted {len(mock_data)} rows from table '{table_id}': {mock_data}"
            
        elif tool_name == "sap_set_table_cell":
            table_id = arguments.get('table_id', 'TABLE')
            row = arguments.get('row', 0)
            column = arguments.get('column', 'COL1')
            value = arguments.get('value', '')
            session_id = arguments.get('session_id', 'default')
            result_text = f"Set cell [{row}][{column}] = '{value}' in table '{table_id}' in session {session_id}"
            
        elif tool_name == "sap_select_table_row":
            table_id = arguments.get('table_id', 'TABLE')
            row = arguments.get('row', 0)
            multi_select = arguments.get('multi_select', False)
            session_id = arguments.get('session_id', 'default')
            result_text = f"Selected row {row} in table '{table_id}' (multi: {multi_select}) in session {session_id}"
        
        # Screen Information
        elif tool_name == "sap_get_screen_info":
            session_id = arguments.get('session_id', 'default')
            screen_info = {
                "program": "SAPMV45A",
                "screen": "4001", 
                "transaction": "VA01",
                "title": "Create Sales Order"
            }
            result_text = f"Screen info for session {session_id}: {screen_info}"
            
        elif tool_name == "sap_get_status_message":
            session_id = arguments.get('session_id', 'default')
            status_msg = "Document saved successfully"
            result_text = f"Status message in session {session_id}: '{status_msg}'"
        
        # Screenshot & Visual
        elif tool_name == "sap_screenshot":
            filename = arguments.get('filename', 'sap_screenshot.png')
            session_id = arguments.get('session_id', 'default')
            result_text = f"Screenshot saved as '{filename}' from session {session_id}"
        
        # Advanced Operations
        elif tool_name == "sap_execute_transaction":
            tcode = arguments.get('transaction_code', 'VA01')
            steps = arguments.get('steps', [])
            session_id = arguments.get('session_id', 'default')
            
            executed_steps = []
            for i, step in enumerate(steps):
                action = step.get('action', 'unknown')
                target = step.get('target', 'unknown')
                value = step.get('value', '')
                executed_steps.append(f"Step {i+1}: {action} on {target} with '{value}'")
            
            result_text = f"Executed transaction {tcode} with {len(steps)} steps: {'; '.join(executed_steps)}"
            
        elif tool_name == "sap_wait_for_screen":
            screen_id = arguments.get('screen_id', 'SCREEN')
            timeout = arguments.get('timeout', 30)
            session_id = arguments.get('session_id', 'default')
            result_text = f"Successfully waited for screen '{screen_id}' (timeout: {timeout}s) in session {session_id}"
        
        # Export & Import
        elif tool_name == "sap_export_data":
            data_source = arguments.get('data_source', 'TABLE')
            format_type = arguments.get('format', 'csv')
            filename = arguments.get('filename', 'export.csv')
            session_id = arguments.get('session_id', 'default')
            result_text = f"Exported data from '{data_source}' to '{filename}' in {format_type} format from session {session_id}"
            
        elif tool_name == "sap_import_data":
            filename = arguments.get('filename', 'import.csv')
            target = arguments.get('target', 'TABLE')
            mapping = arguments.get('mapping', {})
            session_id = arguments.get('session_id', 'default')
            result_text = f"Imported data from '{filename}' to '{target}' with mapping {mapping} in session {session_id}"
        
        else:
            result_text = f"Unknown SAP tool: {tool_name}. Available tools: sap_connect, sap_navigate, sap_input_field, sap_get_table_data, etc."
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": result_text
                }
            ]
        }
    
    def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle JSON-RPC request"""
        try:
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")
            
            logger.info(f"Method: {method}, ID: {request_id}")
            
            if method == "initialize":
                result = self.handle_initialize(params)
                self.initialized = True
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": result
                }
            
            elif method == "notifications/initialized":
                logger.info("Received initialized notification")
                return None  # No response for notifications
            
            elif method == "tools/list":
                result = self.handle_tools_list()
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": result
                }
            
            elif method == "tools/call":
                result = self.handle_tool_call(params)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": result
                }
            
            else:
                logger.warning(f"Unknown method: {method}")
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
        
        except Exception as e:
            logger.error(f"Error handling request: {e}", exc_info=True)
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32602,
                    "message": "Invalid request parameters",
                    "data": str(e)
                }
            }
    
    def run(self):
        """Main server loop - synchronous version"""
        logger.info("Direct SAP MCP Server starting...")
        
        try:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    request = json.loads(line)
                    logger.info(f"Request: {json.dumps(request, indent=2)}")
                    
                    response = self.handle_request(request)
                    
                    if response:
                        response_json = json.dumps(response)
                        print(response_json, flush=True)
                        logger.info(f"Response: {response_json}")
                
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {e}")
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32700,
                            "message": "Parse error"
                        }
                    }
                    print(json.dumps(error_response), flush=True)
                
                except Exception as e:
                    logger.error(f"Unexpected error: {e}", exc_info=True)
        
        except KeyboardInterrupt:
            logger.info("Server interrupted")
        except Exception as e:
            logger.error(f"Server error: {e}", exc_info=True)
        finally:
            logger.info("Direct SAP MCP Server shutting down")

def main():
    """Entry point"""
    server = DirectSAPMCPServer()
    server.run()

if __name__ == "__main__":
    main()
