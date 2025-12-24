#!/bin/bash

# 403 Bypass Practice Lab - Quick Start Script

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     403 Bypass Practice Lab - Quick Start              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment."
        echo "💡 Try installing python3-venv: sudo apt install python3-venv"
        exit 1
    fi
    echo "✅ Virtual environment created!"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not available in virtual environment."
    exit 1
fi

# Upgrade pip, setuptools, and wheel for clean installation
echo "⬆️  Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies."
    echo "💡 Trying without quiet mode to see errors..."
    pip install -r requirements.txt
    exit 1
fi

echo ""
echo "✅ Dependencies installed successfully!"
echo ""
echo "🚀 Starting the server..."
echo ""
echo "📝 The lab will be available at: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

python app.py


