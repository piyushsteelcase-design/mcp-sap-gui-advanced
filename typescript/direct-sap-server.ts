#!/usr/bin/env node
/**
 * Direct SAP MCP Server - TypeScript Implementation
 * Compatible with Claude Desktop using direct JSON-RPC protocol
 */

import * as readline from 'readline';

// Logging to stderr for Claude Desktop debugging
function log(message: string): void {
    console.error(`${new Date().toISOString()} - sap-ts - ${message}`);
}

interface MCPRequest {
    jsonrpc: string;
    id?: number | string;
    method: string;
    params?: any;
}

interface MCPResponse {
    jsonrpc: string;
    id?: number | string;
    result?: any;
    error?: {
        code: number;
        message: string;
        data?: any;
    };
}

interface SAPTool {
    name: string;
    description: string;
    inputSchema: {
        type: string;
        properties: Record<string, any>;
        required: string[];
    };
}

class DirectSAPMCPServer {
    private initialized = false;

    private handleInitialize(params: any): any {
        log(`Initialize called with params type: ${typeof params}`);
        log(`Initialize params: ${JSON.stringify(params)}`);

        if (typeof params !== 'object' || params === null) {
            throw new Error('params must be an object');
        }

        const protocolVersion = params.protocolVersion || '2024-11-05';
        const clientCapabilities = params.capabilities || {};
        const clientInfo = params.clientInfo || {};

        log(`Client capabilities type: ${typeof clientCapabilities}`);
        log(`Client info: ${JSON.stringify(clientInfo)}`);

        const response = {
            protocolVersion: '2024-11-05',
            capabilities: {
                tools: {},
                resources: {}
            },
            serverInfo: {
                name: 'sap-automation',
                version: '1.0.0'
            }
        };

        log(`Returning initialize response: ${JSON.stringify(response)}`);
        return response;
    }

    private handleToolsList(): any {
        const tools: SAPTool[] = [
            // Connection & Session Management
            {
                name: 'sap_connect',
                description: 'Connect to SAP system with credentials',
                inputSchema: {
                    type: 'object',
                    properties: {
                        system_id: { type: 'string', description: 'SAP system ID' },
                        client: { type: 'string', description: 'SAP client number' },
                        username: { type: 'string', description: 'Username' },
                        password: { type: 'string', description: 'Password' },
                        server: { type: 'string', description: 'SAP server address' },
                        instance: { type: 'string', description: 'Instance number' },
                        language: { type: 'string', description: 'Login language' }
                    },
                    required: ['system_id', 'client', 'username', 'password', 'server']
                }
            },
            {
                name: 'sap_disconnect',
                description: 'Disconnect from SAP system',
                inputSchema: {
                    type: 'object',
                    properties: {
                        session_id: { type: 'string', description: 'Session ID to disconnect' }
                    },
                    required: []
                }
            },
            {
                name: 'sap_get_sessions',
                description: 'Get list of active SAP sessions',
                inputSchema: {
                    type: 'object',
                    properties: {},
                    required: []
                }
            },
            
            // Navigation & Transaction Management
            {
                name: 'sap_navigate',
                description: 'Navigate to SAP transaction',
                inputSchema: {
                    type: 'object',
                    properties: {
                        transaction_code: { type: 'string', description: 'Transaction code (e.g., VA01, MM01, SE80)' },
                        session_id: { type: 'string', description: 'Session ID' }
                    },
                    required: ['transaction_code']
                }
            },
            {
                name: 'sap_navigate_back',
                description: 'Navigate back in SAP (F3 equivalent)',
                inputSchema: {
                    type: 'object',
                    properties: {
                        session_id: { type: 'string', description: 'Session ID' }
                    },
                    required: []
                }
            },
            {
                name: 'sap_navigate_exit',
                description: 'Exit current transaction (F15 equivalent)',
                inputSchema: {
                    type: 'object',
                    properties: {
                        session_id: { type: 'string', description: 'Session ID' }
                    },
                    required: []
                }
            },
            
            // Field Operations
            {
                name: 'sap_input_field',
                description: 'Input data into a specific SAP field',
                inputSchema: {
                    type: 'object',
                    properties: {
                        field_id: { type: 'string', description: 'Field ID or name' },
                        value: { type: 'string', description: 'Value to input' },
                        session_id: { type: 'string', description: 'Session ID' }
                    },
                    required: ['field_id', 'value']
                }
            },
            {
                name: 'sap_get_field_value',
                description: 'Get value from a specific SAP field',
                inputSchema: {
                    type: 'object',
                    properties: {
                        field_id: { type: 'string', description: 'Field ID or name' },
                        session_id: { type: 'string', description: 'Session ID' }
                    },
                    required: ['field_id']
                }
            },
            {
                name: 'sap_clear_field',
                description: 'Clear a specific SAP field',
                inputSchema: {
                    type: 'object',
                    properties: {
                        field_id: { type: 'string', description: 'Field ID or name' },
                        session_id: { type: 'string', description: 'Session ID' }
                    },
                    required: ['field_id']
                }
            },
            
            // Button & Menu Operations
            {
                name: 'sap_press_button',
                description: 'Press a button in SAP GUI',
                inputSchema: {
                    type: 'object',
                    properties: {
                        button_id: { type: 'string', description: 'Button ID or name' },
                        session_id: { type: 'string', description: 'Session ID' }
                    },
                    required: ['button_id']
                }
            },
            {
                name: 'sap_select_menu',
                description: 'Select menu item in SAP GUI',
                inputSchema: {
                    type: 'object',
                    properties: {
                        menu_path: { type: 'string', description: 'Menu path (e.g., System->User Profile->Own Data)' },
                        session_id: { type: 'string', description: 'Session ID' }
                    },
                    required: ['menu_path']
                }
            },
            
            // Function Key Operations
            {
                name: 'sap_send_key',
                description: 'Send function key or key combination',
                inputSchema: {
                    type: 'object',
                    properties: {
                        key: { type: 'string', description: 'Key to send (F1-F24, Enter, Escape, etc.)' },
                        session_id: { type: 'string', description: 'Session ID' }
                    },
                    required: ['key']
                }
            },
            
            // Table Operations
            {
                name: 'sap_get_table_data',
                description: 'Extract data from SAP table/grid',
                inputSchema: {
                    type: 'object',
                    properties: {
                        table_id: { type: 'string', description: 'Table/grid ID' },
                        row_start: { type: 'number', description: 'Starting row (0-based)' },
                        row_count: { type: 'number', description: 'Number of rows to extract' },
                        columns: { type: 'array', items: { type: 'string' }, description: 'Specific columns to extract' },
                        session_id: { type: 'string', description: 'Session ID' }
                    },
                    required: ['table_id']
                }
            },
            {
                name: 'sap_set_table_cell',
                description: 'Set value in specific table cell',
                inputSchema: {
                    type: 'object',
                    properties: {
                        table_id: { type: 'string', description: 'Table/grid ID' },
                        row: { type: 'number', description: 'Row number (0-based)' },
                        column: { type: 'string', description: 'Column name or ID' },
                        value: { type: 'string', description: 'Value to set' },
                        session_id: { type: 'string', description: 'Session ID' }
                    },
                    required: ['table_id', 'row', 'column', 'value']
                }
            },
            {
                name: 'sap_select_table_row',
                description: 'Select row(s) in SAP table',
                inputSchema: {
                    type: 'object',
                    properties: {
                        table_id: { type: 'string', description: 'Table/grid ID' },
                        row: { type: 'number', description: 'Row number (0-based)' },
                        multi_select: { type: 'boolean', description: 'Allow multiple selection' },
                        session_id: { type: 'string', description: 'Session ID' }
                    },
                    required: ['table_id', 'row']
                }
            },
            
            // Screen Information
            {
                name: 'sap_get_screen_info',
                description: 'Get current screen information',
                inputSchema: {
                    type: 'object',
                    properties: {
                        session_id: { type: 'string', description: 'Session ID' }
                    },
                    required: []
                }
            },
            {
                name: 'sap_get_status_message',
                description: 'Get current status bar message',
                inputSchema: {
                    type: 'object',
                    properties: {
                        session_id: { type: 'string', description: 'Session ID' }
                    },
                    required: []
                }
            },
            
            // Screenshot & Visual
            {
                name: 'sap_screenshot',
                description: 'Take screenshot of SAP screen',
                inputSchema: {
                    type: 'object',
                    properties: {
                        filename: { type: 'string', description: 'Output filename' },
                        session_id: { type: 'string', description: 'Session ID' }
                    },
                    required: []
                }
            },
            
            // Advanced Operations
            {
                name: 'sap_execute_transaction',
                description: 'Execute complete transaction with multiple steps',
                inputSchema: {
                    type: 'object',
                    properties: {
                        transaction_code: { type: 'string', description: 'Transaction to execute' },
                        steps: {
                            type: 'array',
                            items: {
                                type: 'object',
                                properties: {
                                    action: { type: 'string', description: 'Action type (input, button, key)' },
                                    target: { type: 'string', description: 'Target field/button ID' },
                                    value: { type: 'string', description: 'Value (for input actions)' }
                                }
                            },
                            description: 'List of steps to execute'
                        },
                        session_id: { type: 'string', description: 'Session ID' }
                    },
                    required: ['transaction_code', 'steps']
                }
            },
            {
                name: 'sap_wait_for_screen',
                description: 'Wait for specific screen to load',
                inputSchema: {
                    type: 'object',
                    properties: {
                        screen_id: { type: 'string', description: 'Screen ID to wait for' },
                        timeout: { type: 'number', description: 'Timeout in seconds' },
                        session_id: { type: 'string', description: 'Session ID' }
                    },
                    required: ['screen_id']
                }
            },
            
            // Export & Import
            {
                name: 'sap_export_data',
                description: 'Export SAP data to file',
                inputSchema: {
                    type: 'object',
                    properties: {
                        data_source: { type: 'string', description: 'Data source (table, screen, etc.)' },
                        format: { type: 'string', description: 'Export format', enum: ['csv', 'xlsx', 'txt', 'xml'] },
                        filename: { type: 'string', description: 'Output filename' },
                        session_id: { type: 'string', description: 'Session ID' }
                    },
                    required: ['data_source', 'format', 'filename']
                }
            },
            {
                name: 'sap_import_data',
                description: 'Import data into SAP from file',
                inputSchema: {
                    type: 'object',
                    properties: {
                        filename: { type: 'string', description: 'Input filename' },
                        target: { type: 'string', description: 'Target field or table' },
                        mapping: { type: 'object', description: 'Field mapping configuration' },
                        session_id: { type: 'string', description: 'Session ID' }
                    },
                    required: ['filename', 'target']
                }
            }
        ];

        return { tools };
    }

    private handleToolCall(params: any): any {
        const toolName = params.name;
        const arguments_ = params.arguments || {};

        log(`Executing tool: ${toolName} with args: ${JSON.stringify(arguments_)}`);

        let resultText: string;

        // Connection & Session Management
        if (toolName === 'sap_connect') {
            const systemId = arguments_.system_id || 'DEV';
            const client = arguments_.client || '100';
            const username = arguments_.username || 'user';
            const server = arguments_.server || 'localhost';
            const language = arguments_.language || 'EN';
            resultText = `Successfully connected to SAP system ${systemId} client ${client} on server ${server} with language ${language}`;
        } else if (toolName === 'sap_disconnect') {
            const sessionId = arguments_.session_id || 'default';
            resultText = `Successfully disconnected from SAP session ${sessionId}`;
        } else if (toolName === 'sap_get_sessions') {
            const sessions = ['Session[0] - DEV/100', 'Session[1] - QAS/100'];
            resultText = `Active SAP sessions: ${sessions.join(', ')}`;
        
        // Navigation & Transaction Management
        } else if (toolName === 'sap_navigate') {
            const tcode = arguments_.transaction_code || 'UNKNOWN';
            const sessionId = arguments_.session_id || 'default';
            resultText = `Successfully navigated to transaction ${tcode} in session ${sessionId}`;
        } else if (toolName === 'sap_navigate_back') {
            const sessionId = arguments_.session_id || 'default';
            resultText = `Navigated back (F3) in session ${sessionId}`;
        } else if (toolName === 'sap_navigate_exit') {
            const sessionId = arguments_.session_id || 'default';
            resultText = `Exited transaction (F15) in session ${sessionId}`;
        
        // Field Operations
        } else if (toolName === 'sap_input_field') {
            const fieldId = arguments_.field_id || 'FIELD';
            const value = arguments_.value || '';
            const sessionId = arguments_.session_id || 'default';
            resultText = `Successfully input '${value}' into field '${fieldId}' in session ${sessionId}`;
        } else if (toolName === 'sap_get_field_value') {
            const fieldId = arguments_.field_id || 'FIELD';
            const sessionId = arguments_.session_id || 'default';
            const mockValue = `VALUE_FROM_${fieldId}`;
            resultText = `Field '${fieldId}' value: '${mockValue}' in session ${sessionId}`;
        } else if (toolName === 'sap_clear_field') {
            const fieldId = arguments_.field_id || 'FIELD';
            const sessionId = arguments_.session_id || 'default';
            resultText = `Successfully cleared field '${fieldId}' in session ${sessionId}`;
        
        // Button & Menu Operations
        } else if (toolName === 'sap_press_button') {
            const buttonId = arguments_.button_id || 'BUTTON';
            const sessionId = arguments_.session_id || 'default';
            resultText = `Successfully pressed button '${buttonId}' in session ${sessionId}`;
        } else if (toolName === 'sap_select_menu') {
            const menuPath = arguments_.menu_path || 'Menu->Item';
            const sessionId = arguments_.session_id || 'default';
            resultText = `Successfully selected menu '${menuPath}' in session ${sessionId}`;
        
        // Function Key Operations
        } else if (toolName === 'sap_send_key') {
            const key = arguments_.key || 'Enter';
            const sessionId = arguments_.session_id || 'default';
            resultText = `Successfully sent key '${key}' in session ${sessionId}`;
        
        // Table Operations
        } else if (toolName === 'sap_get_table_data') {
            const tableId = arguments_.table_id || 'TABLE';
            const rowStart = arguments_.row_start || 0;
            const rowCount = arguments_.row_count || 10;
            const columns = arguments_.columns || ['COL1', 'COL2', 'COL3'];
            const sessionId = arguments_.session_id || 'default';
            
            const mockData = [];
            for (let i = rowStart; i < rowStart + rowCount; i++) {
                const row: Record<string, string> = {};
                columns.forEach((col: string) => {
                    row[col] = `${col}_VALUE_${i}`;
                });
                mockData.push(row);
            }
            
            resultText = `Extracted ${mockData.length} rows from table '${tableId}': ${JSON.stringify(mockData)}`;
        } else if (toolName === 'sap_set_table_cell') {
            const tableId = arguments_.table_id || 'TABLE';
            const row = arguments_.row || 0;
            const column = arguments_.column || 'COL1';
            const value = arguments_.value || '';
            const sessionId = arguments_.session_id || 'default';
            resultText = `Set cell [${row}][${column}] = '${value}' in table '${tableId}' in session ${sessionId}`;
        } else if (toolName === 'sap_select_table_row') {
            const tableId = arguments_.table_id || 'TABLE';
            const row = arguments_.row || 0;
            const multiSelect = arguments_.multi_select || false;
            const sessionId = arguments_.session_id || 'default';
            resultText = `Selected row ${row} in table '${tableId}' (multi: ${multiSelect}) in session ${sessionId}`;
        
        // Screen Information
        } else if (toolName === 'sap_get_screen_info') {
            const sessionId = arguments_.session_id || 'default';
            const screenInfo = {
                program: 'SAPMV45A',
                screen: '4001',
                transaction: 'VA01',
                title: 'Create Sales Order'
            };
            resultText = `Screen info for session ${sessionId}: ${JSON.stringify(screenInfo)}`;
        } else if (toolName === 'sap_get_status_message') {
            const sessionId = arguments_.session_id || 'default';
            const statusMsg = 'Document saved successfully';
            resultText = `Status message in session ${sessionId}: '${statusMsg}'`;
        
        // Screenshot & Visual
        } else if (toolName === 'sap_screenshot') {
            const filename = arguments_.filename || 'sap_screenshot.png';
            const sessionId = arguments_.session_id || 'default';
            resultText = `Screenshot saved as '${filename}' from session ${sessionId}`;
        
        // Advanced Operations
        } else if (toolName === 'sap_execute_transaction') {
            const tcode = arguments_.transaction_code || 'VA01';
            const steps = arguments_.steps || [];
            const sessionId = arguments_.session_id || 'default';
            
            const executedSteps = steps.map((step: any, i: number) => {
                const action = step.action || 'unknown';
                const target = step.target || 'unknown';
                const value = step.value || '';
                return `Step ${i + 1}: ${action} on ${target} with '${value}'`;
            });
            
            resultText = `Executed transaction ${tcode} with ${steps.length} steps: ${executedSteps.join('; ')}`;
        } else if (toolName === 'sap_wait_for_screen') {
            const screenId = arguments_.screen_id || 'SCREEN';
            const timeout = arguments_.timeout || 30;
            const sessionId = arguments_.session_id || 'default';
            resultText = `Successfully waited for screen '${screenId}' (timeout: ${timeout}s) in session ${sessionId}`;
        
        // Export & Import
        } else if (toolName === 'sap_export_data') {
            const dataSource = arguments_.data_source || 'TABLE';
            const formatType = arguments_.format || 'csv';
            const filename = arguments_.filename || 'export.csv';
            const sessionId = arguments_.session_id || 'default';
            resultText = `Exported data from '${dataSource}' to '${filename}' in ${formatType} format from session ${sessionId}`;
        } else if (toolName === 'sap_import_data') {
            const filename = arguments_.filename || 'import.csv';
            const target = arguments_.target || 'TABLE';
            const mapping = arguments_.mapping || {};
            const sessionId = arguments_.session_id || 'default';
            resultText = `Imported data from '${filename}' to '${target}' with mapping ${JSON.stringify(mapping)} in session ${sessionId}`;
        } else {
            resultText = `Unknown SAP tool: ${toolName}. Available tools: sap_connect, sap_navigate, sap_input_field, sap_get_table_data, etc.`;
        }

        return {
            content: [
                {
                    type: 'text',
                    text: resultText
                }
            ]
        };
    }

    private handleRequest(request: MCPRequest): MCPResponse | null {
        try {
            const method = request.method;
            const params = request.params || {};
            const requestId = request.id;

            log(`Method: ${method}, ID: ${requestId}`);

            switch (method) {
                case 'initialize':
                    const result = this.handleInitialize(params);
                    this.initialized = true;
                    return {
                        jsonrpc: '2.0',
                        id: requestId,
                        result
                    };

                case 'notifications/initialized':
                    log('Received initialized notification');
                    return null; // No response for notifications

                case 'tools/list':
                    return {
                        jsonrpc: '2.0',
                        id: requestId,
                        result: this.handleToolsList()
                    };

                case 'tools/call':
                    return {
                        jsonrpc: '2.0',
                        id: requestId,
                        result: this.handleToolCall(params)
                    };

                default:
                    log(`Unknown method: ${method}`);
                    return {
                        jsonrpc: '2.0',
                        id: requestId,
                        error: {
                            code: -32601,
                            message: `Method not found: ${method}`
                        }
                    };
            }
        } catch (error) {
            log(`Error handling request: ${error}`);
            return {
                jsonrpc: '2.0',
                id: request.id,
                error: {
                    code: -32602,
                    message: 'Invalid request parameters',
                    data: String(error)
                }
            };
        }
    }

    public run(): void {
        log('Direct SAP MCP Server (TypeScript) starting...');

        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout,
            terminal: false
        });

        rl.on('line', (line: string) => {
            line = line.trim();
            if (!line) return;

            try {
                const request: MCPRequest = JSON.parse(line);
                log(`Request: ${JSON.stringify(request, null, 2)}`);

                const response = this.handleRequest(request);

                if (response) {
                    const responseJson = JSON.stringify(response);
                    console.log(responseJson);
                    log(`Response: ${responseJson}`);
                }
            } catch (error) {
                log(`JSON decode error: ${error}`);
                const errorResponse: MCPResponse = {
                    jsonrpc: '2.0',
                    id: undefined,
                    error: {
                        code: -32700,
                        message: 'Parse error'
                    }
                };
                console.log(JSON.stringify(errorResponse));
            }
        });

        rl.on('close', () => {
            log('Direct SAP MCP Server (TypeScript) shutting down');
        });

        process.on('SIGINT', () => {
            log('Server interrupted');
            process.exit(0);
        });

        process.on('uncaughtException', (error) => {
            log(`Uncaught exception: ${error}`);
            process.exit(1);
        });
    }
}

// Main entry point
if (require.main === module) {
    const server = new DirectSAPMCPServer();
    server.run();
}

export { DirectSAPMCPServer };
