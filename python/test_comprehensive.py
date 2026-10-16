#!/usr/bin/env python3
"""
Test comprehensive SAP tools in the MCP server
"""

from direct_sap_server import DirectSAPMCPServer
import json
import sys


def _configure_stdout_utf8() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

def test_comprehensive_tools():
    """Test that all comprehensive SAP tools are available"""
    _configure_stdout_utf8()
    print("Testing comprehensive SAP MCP server...")
    
    server = DirectSAPMCPServer()
    
    # Test tools list
    tools_result = server.handle_tools_list()
    tools = tools_result.get("tools", [])
    
    print(f"✅ Number of SAP tools available: {len(tools)}")
    print("\n📋 Available SAP Tools:")
    
    # Group tools by category
    categories = {
        "Connection & Session": ["sap_connect", "sap_disconnect", "sap_get_sessions"],
        "Navigation": ["sap_navigate", "sap_navigate_back", "sap_navigate_exit"],
        "Field Operations": ["sap_input_field", "sap_get_field_value", "sap_clear_field"],
        "Button & Menu": ["sap_press_button", "sap_select_menu"],
        "Function Keys": ["sap_send_key"],
        "Table Operations": ["sap_get_table_data", "sap_set_table_cell", "sap_select_table_row"],
        "Screen Info": ["sap_get_screen_info", "sap_get_status_message"],
        "Visual": ["sap_screenshot"],
        "Advanced": ["sap_execute_transaction", "sap_wait_for_screen"],
        "Data Exchange": ["sap_export_data", "sap_import_data"],
        "Agent-based Tests": ["sap_dynamic_login", "sap_run_test"]
    }
    
    available_tools = [tool["name"] for tool in tools]
    
    for category, tool_names in categories.items():
        print(f"\n🔧 {category}:")
        for tool_name in tool_names:
            if tool_name in available_tools:
                tool_info = next(t for t in tools if t["name"] == tool_name)
                print(f"   ✅ {tool_name} - {tool_info['description']}")
            else:
                print(f"   ❌ {tool_name} - MISSING")
    
    # Test a few tool calls
    print(f"\n🧪 Testing tool execution:")
    
    # Test connection
    connect_result = server.handle_tool_call({
        "name": "sap_connect",
        "arguments": {"system_id": "DEV", "client": "100", "username": "testuser", "password": "pass", "server": "sap-server"}
    })
    print(f"✅ Connect: {connect_result['content'][0]['text']}")
    
    # Test navigation
    nav_result = server.handle_tool_call({
        "name": "sap_navigate", 
        "arguments": {"transaction_code": "VA01"}
    })
    print(f"✅ Navigate: {nav_result['content'][0]['text']}")
    
    # Test field input
    field_result = server.handle_tool_call({
        "name": "sap_input_field",
        "arguments": {"field_id": "VBAK-VKORG", "value": "1000"}
    })
    print(f"✅ Field Input: {field_result['content'][0]['text']}")
    
    # Test table data
    table_result = server.handle_tool_call({
        "name": "sap_get_table_data",
        "arguments": {"table_id": "SALES_TABLE", "row_count": 3}
    })
    print(f"✅ Table Data: {table_result['content'][0]['text'][:100]}...")
    
    # Test advanced transaction
    exec_result = server.handle_tool_call({
        "name": "sap_execute_transaction",
        "arguments": {
            "transaction_code": "VA01",
            "steps": [
                {"action": "input", "target": "VBAK-VKORG", "value": "1000"},
                {"action": "button", "target": "SAVE", "value": ""}
            ]
        }
    })
    print(f"✅ Execute Transaction: {exec_result['content'][0]['text']}")

    # Test sap_run_test success path
    run_test_result = server.handle_tool_call({
        "name": "sap_run_test",
        "arguments": {"test_type": "full"}
    })
    run_test_text = run_test_result["content"][0]["text"]
    if "test completed successfully" not in run_test_text:
        raise AssertionError(f"sap_run_test full failed: {run_test_text}")
    print(f"✅ sap_run_test (full): {run_test_text.splitlines()[0]}")

    # Test sap_run_test invalid input handling
    invalid_test_result = server.handle_tool_call({
        "name": "sap_run_test",
        "arguments": {"test_type": "invalid"}
    })
    invalid_test_text = invalid_test_result["content"][0]["text"]
    if "Unsupported test_type" not in invalid_test_text:
        raise AssertionError(
            f"sap_run_test invalid input handling failed: {invalid_test_text}"
        )
    print("✅ sap_run_test invalid input handling: returns explicit error message")
    
    print(f"\n🎉 SUCCESS: All {len(tools)} SAP automation tools are working!")
    return True

if __name__ == "__main__":
    test_comprehensive_tools()
