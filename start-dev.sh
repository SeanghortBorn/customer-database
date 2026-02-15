#!/bin/bash

# Customer Database System - Development Startup Script

set -e

echo "🚀 Starting Customer Database System..."
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running from project root
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo -e "${RED}Error: Please run this script from the project root directory${NC}"
    exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command_exists python3; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

if ! command_exists node; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites check passed${NC}"
echo ""

# Backend setup
echo -e "${BLUE}Setting up backend...${NC}"
cd backend

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}Warning: .env file not found in backend/. Creating from example...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${RED}Please edit backend/.env with your credentials before continuing${NC}"
        exit 1
    fi
fi

# Check if virtual environment exists or conda is active
if [ -z "$CONDA_DEFAULT_ENV" ] && [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating Python virtual environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run migrations
echo -e "${BLUE}Running database migrations...${NC}"
alembic upgrade head

# Start backend in background
echo -e "${BLUE}Starting backend server...${NC}"
python api_gateway/main.py &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"

cd ..

# Frontend setup
echo -e "${BLUE}Setting up frontend...${NC}"
cd frontend

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo -e "${RED}Warning: .env.local file not found in frontend/. Creating from example...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env.local
        echo -e "${RED}Please edit frontend/.env.local with your credentials${NC}"
    fi
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}Installing frontend dependencies...${NC}"
    npm install
fi

# Start frontend
echo -e "${BLUE}Starting frontend server...${NC}"
npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"

cd ..

echo ""
echo -e "${GREEN}✅ Customer Database System is running!${NC}"
echo ""
echo "📍 Access points:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${BLUE}Stopping services...${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo -e "${GREEN}Services stopped${NC}"
    exit 0
}

# Trap SIGINT and SIGTERM
trap cleanup INT TERM

# Wait for processes
wait
