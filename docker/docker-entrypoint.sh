#!/bin/bash

echo "🐳 Starting Enterprise Agent in Docker..."

# Wait for any dependencies
sleep 2

# Check environment
if [ -z "$GEMINI_API_KEY" ] || [ "$GEMINI_API_KEY" = "your-gemini-api-key-here" ]; then
    echo "⚠️  Warning: GEMINI_API_KEY not set properly"
fi

# Create required directories
mkdir -p data logs

# Start the application
echo "🚀 Starting agent API server..."
exec python -m uvicorn api:app --host 0.0.0.0 --port 8000