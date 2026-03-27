#!/bin/bash

# Plan Your Study - Quick Start Script
# This script sets up and runs the entire application

set -e

echo "=========================================="
echo "Plan Your Study - Quick Start"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.8+"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm is required but not installed. Please install Node.js"
    exit 1
fi

echo -e "${GREEN}✓ Python found: $(python3 --version)${NC}"
echo -e "${GREEN}✓ npm found: $(npm --version)${NC}"
echo ""

# Setup Backend
echo -e "${BLUE}Setting up backend...${NC}"

cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

# Copy env file if needed
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
fi

echo -e "${GREEN}✓ Backend setup complete${NC}"
echo ""

# Setup Frontend
echo -e "${BLUE}Setting up frontend...${NC}"

cd ../frontend

echo "Installing npm dependencies..."
npm install --quiet

# Copy env file if needed
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file from template..."
    cp .env.example .env.local
fi

echo -e "${GREEN}✓ Frontend setup complete${NC}"
echo ""

# Instructions for running
echo -e "${YELLOW}=========================================="
echo "Setup Complete! 🎉"
echo "==========================================${NC}"
echo ""
echo "To start the application, open TWO terminal windows:"
echo ""
echo -e "${BLUE}Terminal 1 - Backend:${NC}"
echo "  cd backend"
echo "  source venv/bin/activate  # or: venv\\Scripts\\activate on Windows"
echo "  python main.py"
echo ""
echo -e "${BLUE}Terminal 2 - Frontend:${NC}"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo -e "${YELLOW}Then open your browser:${NC}"
echo "  Frontend: http://localhost:3000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "For detailed instructions, see SETUP_GUIDE.md"
echo ""
