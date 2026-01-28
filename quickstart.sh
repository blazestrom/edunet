#!/bin/bash
# Quick Start Script for Lecture Voice-to-Notes Generator
# Run this script to set up and start the application

echo "🎓 Lecture Voice-to-Notes Generator - Quick Start"
echo "=================================================="
echo ""

# Check Python installation
echo "✓ Checking Python installation..."
python --version
if [ $? -ne 0 ]; then
    echo "❌ Python not found. Please install Python 3.8+"
    exit 1
fi

# Install dependencies
echo ""
echo "✓ Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Check for .env file
echo ""
echo "✓ Checking environment configuration..."
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env and add your OPENAI_API_KEY"
    echo "   You can get one at: https://platform.openai.com/account/api-keys"
    echo ""
    read -p "Press Enter after updating .env file..."
fi

# Verify OpenAI API Key
if grep -q "OPENAI_API_KEY=your_openai_api_key_here" .env; then
    echo "❌ Please update OPENAI_API_KEY in .env file!"
    exit 1
fi

# Create output directories
echo ""
echo "✓ Creating output directories..."
mkdir -p uploads
mkdir -p output

# Start the server
echo ""
echo "✓ Starting server..."
echo "=================================================="
echo ""
echo "🚀 Server is running!"
echo ""
echo "Access the application at:"
echo "  • Web Interface: http://localhost:8000/test"
echo "  • API Docs: http://localhost:8000/docs"
echo "  • ReDoc: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "=================================================="
echo ""

python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
