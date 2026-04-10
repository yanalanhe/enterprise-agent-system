#!/bin/bash

echo "🔍 Verifying Enterprise Agent Setup..."

# Check Python dependencies
echo "📦 Checking Python dependencies..."
cd backend
python -c "
import fastapi, uvicorn, pydantic, cryptography, sqlalchemy
import structlog, typer, rich
print('✅ All Python dependencies installed')
" || echo "❌ Missing Python dependencies"

# Check Node dependencies  
echo "🌐 Checking Node dependencies..."
cd ../frontend
if [ -d "node_modules" ]; then
    echo "✅ Node dependencies installed"
else
    echo "❌ Node dependencies missing"
fi

# Check file structure
echo "📁 Verifying file structure..."
cd ..
required_files=(
    "backend/src/agent/core.py"
    "backend/src/utils/encryption.py" 
    "backend/src/utils/logger.py"
    "backend/src/cli.py"
    "backend/src/api.py"
    "frontend/src/App.js"
    "frontend/src/components/Dashboard.js"
    "docker-compose.yml"
    "start.sh"
    "stop.sh"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ Missing: $file"
    fi
done

echo "🎯 Setup verification complete!"