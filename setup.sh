#!/bin/bash

# SAP MCP Server - Automated Setup Script
# This script sets up the SAP MCP Server on a new machine

echo "🚀 SAP MCP Server Setup Script"
echo "=============================="

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: Please run this script from the SAP MCP Server root directory"
    exit 1
fi

echo "📋 Choose implementation:"
echo "1) Python (Recommended - No dependencies)"
echo "2) TypeScript (Advanced - Requires Node.js)"
echo "3) Both implementations"
read -p "Enter choice (1-3): " choice

case $choice in
    1|3)
        echo ""
        echo "🐍 Setting up Python implementation..."
        cd python
        
        # Check Python version
        if command -v python3 &> /dev/null; then
            PYTHON_CMD="python3"
        elif command -v python &> /dev/null; then
            PYTHON_CMD="python"
        else
            echo "❌ Error: Python not found. Please install Python 3.7+"
            exit 1
        fi
        
        echo "✅ Python found: $($PYTHON_CMD --version)"
        
        # Test the server
        echo "🧪 Testing Python server..."
        if $PYTHON_CMD test_comprehensive.py; then
            echo "✅ Python server test passed!"
        else
            echo "❌ Python server test failed"
            exit 1
        fi
        
        cd ..
        ;;
esac

case $choice in
    2|3)
        echo ""
        echo "📦 Setting up TypeScript implementation..."
        cd typescript
        
        # Check Node.js
        if ! command -v node &> /dev/null; then
            echo "❌ Error: Node.js not found. Please install Node.js 18+"
            exit 1
        fi
        
        echo "✅ Node.js found: $(node --version)"
        
        # Install dependencies
        echo "📦 Installing dependencies..."
        if npm install; then
            echo "✅ Dependencies installed successfully"
        else
            echo "❌ Failed to install dependencies"
            exit 1
        fi
        
        # Build project
        echo "🔨 Building TypeScript project..."
        if npm run build; then
            echo "✅ TypeScript build successful"
        else
            echo "❌ TypeScript build failed"
            exit 1
        fi
        
        # Test the server
        echo "🧪 Testing TypeScript server..."
        if node test-comprehensive.js; then
            echo "✅ TypeScript server test passed!"
        else
            echo "❌ TypeScript server test failed"
            exit 1
        fi
        
        cd ..
        ;;
esac

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Copy the appropriate claude-desktop configuration:"

if [ $choice -eq 1 ] || [ $choice -eq 3 ]; then
    echo "   Python: cp python/claude_desktop_direct.json ~/.config/claude/claude_desktop_config.json"
fi

if [ $choice -eq 2 ] || [ $choice -eq 3 ]; then
    echo "   TypeScript: cp typescript/claude-desktop-config.json ~/.config/claude/claude_desktop_config.json"
fi

echo "2. Restart Claude Desktop"
echo "3. Ask Claude: 'List all available SAP automation tools'"
echo ""
echo "✅ Your SAP MCP Server with 22 automation tools is ready!"
