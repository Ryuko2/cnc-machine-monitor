#!/bin/bash

# CNC Machine Monitor - Green Theme Edition
# Startup Script for Mac/Linux

echo "=========================================="
echo "CNC Machine Monitor - Green Theme"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null
then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if backend exists
if [ ! -f "backend/api.py" ]; then
    echo "❌ Error: backend/api.py not found"
    echo "Please run this script from the complete-green-deployment folder"
    exit 1
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install fastapi uvicorn websockets --break-system-packages > /dev/null 2>&1

echo ""
echo "✅ Setup complete!"
echo ""
echo "=========================================="
echo "Starting CNC Machine Monitor..."
echo "=========================================="
echo ""
echo "Backend API: http://localhost:5000"
echo "Dashboard:   http://localhost:5000"
echo ""
echo "To access from phone:"
echo "1. Find your computer's IP (run 'ifconfig | grep inet')"
echo "2. Open browser on phone to: http://YOUR-IP:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "=========================================="
echo ""

# Start the server
cd backend
python3 api.py
