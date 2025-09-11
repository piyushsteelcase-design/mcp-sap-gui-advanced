#!/usr/bin/env node
/**
 * Test the Direct SAP MCP Server (TypeScript)
 */

import { spawn } from 'child_process';
import * as path from 'path';

function testDirectServer(): void {
    console.log('Testing Direct SAP MCP Server (TypeScript)...');

    const serverPath = path.join(__dirname, 'direct-sap-server.js');
    
    const server = spawn('node', [serverPath], {
        stdio: ['pipe', 'pipe', 'pipe'],
    });

    let responseCount = 0;
    const expectedResponses = 3;

    server.stdout.on('data', (data) => {
        const response = data.toString().trim();
        console.log(`Response ${++responseCount}: ${response}`);
        
        if (responseCount >= expectedResponses) {
            console.log('✅ TypeScript server test completed successfully!');
            server.kill();
        }
    });

    server.stderr.on('data', (data) => {
        console.log(`Server log: ${data.toString().trim()}`);
    });

    server.on('error', (error) => {
        console.error(`❌ Test failed: ${error.message}`);
    });

    // Send test requests
    setTimeout(() => {
        // Initialize
        const initRequest = {
            jsonrpc: '2.0',
            id: 1,
            method: 'initialize',
            params: {
                protocolVersion: '2024-11-05',
                capabilities: { tools: {}, resources: {} },
                clientInfo: { name: 'test-client', version: '1.0.0' }
            }
        };

        console.log('Sending initialize request...');
        server.stdin.write(JSON.stringify(initRequest) + '\n');

        setTimeout(() => {
            // Tools list
            const toolsRequest = {
                jsonrpc: '2.0',
                id: 2,
                method: 'tools/list'
            };

            console.log('Sending tools/list request...');
            server.stdin.write(JSON.stringify(toolsRequest) + '\n');

            setTimeout(() => {
                // Tool call
                const toolRequest = {
                    jsonrpc: '2.0',
                    id: 3,
                    method: 'tools/call',
                    params: {
                        name: 'sap_screenshot'
                    }
                };

                console.log('Sending tool call...');
                server.stdin.write(JSON.stringify(toolRequest) + '\n');
            }, 100);
        }, 100);
    }, 100);
}

if (require.main === module) {
    testDirectServer();
}
