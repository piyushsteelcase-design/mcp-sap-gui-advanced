#!/bin/bash

# Quick Setup Script for SAP MCP Server
# This script helps users configure the MCP server after cloning

echo "🚀 SAP MCP Server - Quick Setup"
echo "================================"

# Get the current directory
CURRENT_DIR=$(pwd)
echo "📁 Project directory: $CURRENT_DIR"

# Detect OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    OS="windows"
    CONFIG_DIR="$APPDATA/Claude"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    CONFIG_DIR="$HOME/.config/claude"
else
    OS="linux"
    CONFIG_DIR="$HOME/.config/claude"
fi

echo "🖥️  Detected OS: $OS"

# Choose implementation
echo ""
echo "Choose implementation:"
echo "1) Python (Recommended - no dependencies)"
echo "2) TypeScript (requires Node.js)"
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo "🐍 Setting up Python implementation..."
        IMPL_DIR="$CURRENT_DIR/python"
        CONFIG_FILE="claude_desktop_direct.json"
        SERVER_FILE="direct_sap_server.py"
        COMMAND="python"
        
        # Test Python
        cd python
        echo "🧪 Testing Python server..."
        python test_direct.py
        cd ..
        ;;
    2)
        echo "📦 Setting up TypeScript implementation..."
        IMPL_DIR="$CURRENT_DIR/typescript"
        CONFIG_FILE="claude-desktop-config.json"
        SERVER_FILE="direct-sap-server.js"
        COMMAND="node"
        
        # Install dependencies and build
        cd typescript
        echo "📦 Installing dependencies..."
        npm install
        echo "🔨 Building project..."
        npm run build
        echo "🧪 Testing TypeScript server..."
        npm test
        cd ..
        ;;
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac

# Create Claude config directory if it doesn't exist
mkdir -p "$CONFIG_DIR"

# Generate the correct configuration
echo "⚙️  Generating Claude Desktop configuration..."

cat > "$CONFIG_DIR/claude_desktop_config.json" << EOF
{
  "mcpServers": {
    "sap-automation": {
      "command": "$COMMAND",
      "args": ["$IMPL_DIR/$SERVER_FILE"],
      "cwd": "$IMPL_DIR"
    }
  }
}
EOF

echo "✅ Configuration created at: $CONFIG_DIR/claude_desktop_config.json"
echo ""
echo "🎉 Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Restart Claude Desktop"
echo "2. Ask Claude: 'List all available SAP automation tools'"
echo "3. You should see 22 SAP automation tools available"
echo ""
echo "📖 For manual setup instructions, see SETUP.md"
