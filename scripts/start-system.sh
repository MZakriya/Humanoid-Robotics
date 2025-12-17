#!/bin/bash

# Physical AI & Humanoid Robotics System Startup Script
# This script starts both the backend and frontend servers

echo "Starting Physical AI & Humanoid Robotics System..."
echo

# Check if backend directory exists
if [ ! -d "backend" ]; then
    echo "Error: Backend directory not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Check if frontend dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "Error installing frontend dependencies"
        exit 1
    fi
fi

# Create backend virtual environment if it doesn't exist
if [ ! -d "backend/venv" ]; then
    echo "Creating backend virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    cd ..
fi

# Start backend server in background
echo "Starting backend server..."
cd backend
source venv/bin/activate
cd src &
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ../..

# Wait a moment for backend to start
sleep 5

# Start frontend server in background
echo "Starting frontend server..."
npm run start &
FRONTEND_PID=$!

# Function to stop servers
cleanup() {
    echo
    echo "Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Trap Ctrl+C to clean up
trap cleanup INT

echo
echo "System started successfully!"
echo
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo
echo "Press Ctrl+C to stop the servers..."

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID