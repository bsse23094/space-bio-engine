#!/bin/bash

# Space Biology Knowledge Engine - Backend Startup Script
# This script sets up and runs the FastAPI backend server

echo "🚀 Starting Space Biology Knowledge Engine Backend..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        print_error "Python is not installed. Please install Python 3.8+ and try again."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
print_success "Python $PYTHON_VERSION found"

# Check if we're in the Backend directory
if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found. Please run this script from the Backend directory."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    if [ $? -eq 0 ]; then
        print_success "Virtual environment created"
    else
        print_error "Failed to create virtual environment"
        exit 1
    fi
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

if [ $? -eq 0 ]; then
    print_success "Virtual environment activated"
else
    print_error "Failed to activate virtual environment"
    exit 1
fi

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    print_success "Dependencies installed successfully"
else
    print_warning "Some dependencies may have failed to install. Continuing anyway..."
fi

# Check if data files exist
print_status "Checking data files..."
DATA_FILES=(
    "../datasets/sb_publications_clean.csv"
    "../datasets/topics.csv"
    "../datasets/embeddings.npy"
    "../datasets/metadata.json"
)

MISSING_FILES=()
for file in "${DATA_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -eq 0 ]; then
    print_success "All data files found"
else
    print_warning "Some data files are missing:"
    for file in "${MISSING_FILES[@]}"; do
        echo "  - $file"
    done
    print_warning "The API will run with limited functionality"
fi

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export API_HOST="0.0.0.0"
export API_PORT="8000"
export API_DEBUG="True"

# Create logs directory if it doesn't exist
mkdir -p logs

# Start the server
print_status "Starting FastAPI server..."
print_status "Server will be available at:"
echo "  📖 API Documentation: http://localhost:8000/docs"
echo "  📚 Alternative Docs: http://localhost:8000/redoc"
echo "  ❤️  Health Check: http://localhost:8000/health"
echo "  📊 API Stats: http://localhost:8000/api/v1/stats"
echo ""
print_status "Press Ctrl+C to stop the server"
echo ""

# Start uvicorn server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level info

# If uvicorn fails, try alternative startup
if [ $? -ne 0 ]; then
    print_warning "Uvicorn failed, trying alternative startup method..."
    $PYTHON_CMD -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
fi