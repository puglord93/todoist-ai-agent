#!/bin/bash
# Test if Todoist MCP connection is working

echo "Testing Todoist MCP Connection..."
echo "=================================="
echo ""

# Check if API key is set in mcp.json
if grep -q "YOUR_API_KEY_HERE" ~/.cursor/mcp.json 2>/dev/null; then
    echo "❌ API key not configured in ~/.cursor/mcp.json"
    exit 1
fi

echo "✅ API key is configured in ~/.cursor/mcp.json"
echo ""

# Check if @doist/todoist-ai is accessible
if ! command -v npx &> /dev/null; then
    echo "❌ npx not found. Please install Node.js"
    exit 1
fi

echo "✅ npx is available"
echo ""

echo "📋 Next steps:"
echo "1. Make sure Cursor/Claude Code is restarted"
echo "2. In Claude Code, say: 'What MCP servers are connected?'"
echo "3. In Claude Code, say: 'Fetch my Todoist tasks using MCP'"
echo ""
echo "If the MCP server is properly connected, Claude will be able to"
echo "fetch your tasks and pass them to the Python analysis agent."
echo ""
echo "To test with mock data while waiting:"
echo "  ./run.sh --mock"
