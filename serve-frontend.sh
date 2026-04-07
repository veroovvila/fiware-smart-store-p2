#!/bin/bash
# Simple HTTP Server for Frontend Development
# Start frontend development server on port 8000

cd "$(dirname "$0")/frontend"

echo "🚀 Starting Frontend Server..."
echo "📍 URL: http://localhost:8000"
echo "ℹ️  Backend should be running on http://localhost:5000"
echo "ℹ️  Press Ctrl+C to stop the server"
echo ""

# Check if Python is available
if command -v python3 &> /dev/null; then
    python3 -m http.server 8000 --bind 127.0.0.1
elif command -v python &> /dev/null; then
    python -m http.server 8000 --bind 127.0.0.1
else
    echo "❌ Error: Python not found. Please install Python or use another HTTP server."
    echo "   Alternatives:"
    echo "   - npm install -g live-server && live-server"
    echo "   - Open frontend/index.html directly in your browser"
    exit 1
fi
