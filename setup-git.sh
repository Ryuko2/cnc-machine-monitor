#!/bin/bash

# CNC Machine Monitor - GitHub Setup Script
# This script prepares your project for GitHub

echo "=========================================="
echo "CNC Machine Monitor - GitHub Setup"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}⚠️  Git is not installed!${NC}"
    echo "Please install Git first:"
    echo "  - Windows: Download from https://git-scm.com/download/win"
    echo "  - Mac: brew install git"
    echo "  - Linux: sudo apt install git"
    exit 1
fi

echo -e "${GREEN}✓${NC} Git is installed"
echo ""

# Check if this is already a git repository
if [ -d .git ]; then
    echo -e "${YELLOW}⚠️  This is already a Git repository${NC}"
    echo ""
    read -p "Do you want to reinitialize? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf .git
        echo -e "${GREEN}✓${NC} Removed existing Git repository"
    else
        echo "Keeping existing repository"
        exit 0
    fi
fi

# Initialize git repository
echo -e "${BLUE}Initializing Git repository...${NC}"
git init
echo -e "${GREEN}✓${NC} Git repository initialized"
echo ""

# Set default branch to main
git branch -M main
echo -e "${GREEN}✓${NC} Default branch set to 'main'"
echo ""

# Add all files
echo -e "${BLUE}Adding files to Git...${NC}"
git add .
echo -e "${GREEN}✓${NC} Files added"
echo ""

# Create initial commit
echo -e "${BLUE}Creating initial commit...${NC}"
git commit -m "Initial commit: CNC Machine Monitor v1.0.0

Features:
- Real-time machine monitoring via WebSocket
- Support for 5 machine types
- SQLite database for historical data
- REST API with comprehensive endpoints
- Mobile-responsive dashboard
- Cross-platform support (Windows/Mac/Linux)
- Docker support
- Comprehensive documentation"

echo -e "${GREEN}✓${NC} Initial commit created"
echo ""

# Display next steps
echo "=========================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Create a new repository on GitHub:"
echo "   - Go to https://github.com/new"
echo "   - Name: cnc-machine-monitor"
echo "   - Description: Real-time CNC machine monitoring dashboard"
echo "   - Keep it Public or Private"
echo "   - DON'T initialize with README, .gitignore, or license"
echo ""
echo "2. Connect to GitHub and push:"
echo "   ${BLUE}git remote add origin https://github.com/YOUR-USERNAME/cnc-machine-monitor.git${NC}"
echo "   ${BLUE}git push -u origin main${NC}"
echo ""
echo "3. Optional - Add topics to your GitHub repo:"
echo "   - cnc"
echo "   - manufacturing"
echo "   - iot"
echo "   - monitoring"
echo "   - fastapi"
echo "   - websocket"
echo ""
echo "4. Update README.md with your GitHub username"
echo ""
echo "=========================================="
echo ""
echo "For detailed deployment instructions, see:"
echo "  - INSTALLATION.md"
echo "  - DEPLOYMENT.md"
echo "  - API_DOCUMENTATION.md"
echo ""
