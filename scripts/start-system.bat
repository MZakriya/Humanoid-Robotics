@echo off
REM Physical AI & Humanoid Robotics System Startup Script
REM This script starts both the backend and frontend servers

echo Starting Physical AI & Humanoid Robotics System...
echo.

REM Check if backend directory exists
if not exist "backend" (
    echo Error: Backend directory not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

REM Check if frontend dependencies are installed
if not exist "node_modules" (
    echo Installing frontend dependencies...
    npm install
    if errorlevel 1 (
        echo Error installing frontend dependencies
        pause
        exit /b 1
    )
)

REM Start backend server in a new window
echo Starting backend server...
start "Backend Server" cmd /k "cd backend && if not exist venv python -m venv venv && call venv\Scripts\activate && cd src && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait a moment for backend to start
timeout /t 5 /nobreak >nul

REM Start frontend server in a new window
echo Starting frontend server...
start "Frontend Server" cmd /k "npm run start"

echo.
echo System started successfully!
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause >nul