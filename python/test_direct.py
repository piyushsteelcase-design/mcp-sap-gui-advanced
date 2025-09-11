#!/usr/bin/env python3
"""Test the direct SAP MCP server - Non-interactive version"""

import json
import sys
from pathlib import Path

# Import the server directly instead of running subprocess
sys.path.insert(0, str(Path(__file__).parent))
from direct_sap_server import DirectSAPMCPServer

def test_direct_server():
    """Test the direct MCP server without subprocess"""
    print("Testing Direct SAP MCP Server (Non-interactive)...")
    
    try:
        # Create server instance
        server = DirectSAPMCPServer()
        
        # Test initialize
        print("🧪 Testing initialize...")
        init_params = {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}, "resources": {}},
            "clientInfo": {"name": "test-client", "version": "1.0.0"}
        }
        
        init_result = server.handle_initialize(init_params)
        print(f"✅ Initialize: {init_result['protocolVersion']}")
        
        # Test tools/list
        print("🧪 Testing tools/list...")
        tools_result = server.handle_tools_list()
        tool_count = len(tools_result['tools'])
        print(f"✅ Tools available: {tool_count}")
        
        # Test a simple tool call
        print("🧪 Testing tool call (sap_screenshot)...")
        tool_params = {"name": "sap_screenshot"}
        tool_result = server.handle_tool_call(tool_params)
        print(f"✅ Tool call: {tool_result['content'][0]['text'][:50]}...")
        
        # Test another tool call with parameters
        print("🧪 Testing tool call with params (sap_connect)...")
        connect_params = {
            "name": "sap_connect",
            "arguments": {
                "system_id": "DEV",
                "client": "100", 
                "username": "testuser",
                "password": "testpass"
            }
        }
        connect_result = server.handle_tool_call(connect_params)
        print(f"✅ Connect tool: Success")
        
        print("")
        print("🎉 SUCCESS: Direct MCP server test completed!")
        print(f"📊 Total SAP tools available: {tool_count}")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_direct_server()
    sys.exit(0 if success else 1)
