#!/bin/bash

# Space Biology Knowledge Engine - Full Application Startup (Linux/Mac)
# This script starts both backend and frontend servers

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================"
echo " Space Biology Knowledge Engine"
echo " Full Application Startup"
echo "========================================"
echo ""

# Check if running from project root
if [ ! -d "Backend" ]; then
    echo -e "${RED}[ERROR]${NC} Please run this script from the project root directory"
    echo "Current directory: $(pwd)"
    exit 1
fi

if [ ! -d "Frontend" ]; then
    echo -e "${RED}[ERROR]${NC} Frontend directory not found"
    exit 1
fi

echo -e "${BLUE}[INFO]${NC} Starting Space Biology Knowledge Engine..."
echo ""

# Step 1: Start Backend
echo -e "${BLUE}=== Step 1: Starting Backend Server ===${NC}"
cd Backend

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}[INFO]${NC} Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment and install dependencies
source .venv/bin/activate
echo -e "${GREEN}[SUCCESS]${NC} Virtual environment activated"
echo -e "${BLUE}[INFO]${NC} Installing backend dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Start backend server in background
echo -e "${GREEN}[INFO]${NC} Starting backend server on http://localhost:8000"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo -e "${GREEN}[SUCCESS]${NC} Backend server starting (PID: $BACKEND_PID)..."
sleep 5
cd ..

# Step 2: Start Frontend
echo ""
echo -e "${BLUE}=== Step 2: Starting Frontend Application ===${NC}"
cd Frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}[INFO]${NC} Installing frontend dependencies..."
    npm install
else
    echo -e "${GREEN}[INFO]${NC} Dependencies already installed"
fi

# Start frontend server in background
echo -e "${GREEN}[INFO]${NC} Starting frontend server on http://localhost:4200"
npm start &
FRONTEND_PID=$!

cd ..

# Summary
echo ""
echo "========================================"
echo -e " ${GREEN}Application Started Successfully!${NC}"
echo "========================================"
echo ""
echo -e "${BLUE}Backend API:${NC}"
echo "  - API Server: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Health: http://localhost:8000/health"
echo ""
echo -e "${BLUE}Frontend App:${NC}"
echo "  - Application: http://localhost:4200"
echo ""
echo -e "${YELLOW}[INFO]${NC} Backend PID: $BACKEND_PID"
echo -e "${YELLOW}[INFO]${NC} Frontend PID: $FRONTEND_PID"
echo ""
echo "To stop the servers, run:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo -e "${GREEN}[SUCCESS]${NC} Application is running!"
echo ""
echo "Press Ctrl+C to stop both servers..."

# Wait for processes
wait
