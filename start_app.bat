@echo off
REM Space Biology Knowledge Engine - Full Application Startup (Windows)
REM This script starts both backend and frontend servers

echo ========================================
echo  Space Biology Knowledge Engine
echo  Full Application Startup
echo ========================================
echo.

REM Colors for output
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "RED=[91m"
set "NC=[0m"

REM Check if running from project root
if not exist "Backend\" (
    echo %RED%[ERROR]%NC% Please run this script from the project root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

if not exist "Frontend\" (
    echo %RED%[ERROR]%NC% Frontend directory not found
    pause
    exit /b 1
)

echo %BLUE%[INFO]%NC% Starting Space Biology Knowledge Engine...
echo.

REM Step 1: Start Backend
echo %BLUE%=== Step 1: Starting Backend Server ===%NC%
cd Backend

REM Check if virtual environment exists
if not exist ".venv\" (
    echo %YELLOW%[INFO]%NC% Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment and install dependencies
call .venv\Scripts\activate.bat
echo %GREEN%[SUCCESS]%NC% Virtual environment activated
echo %BLUE%[INFO]%NC% Installing backend dependencies...
.venv\Scripts\python.exe -m pip install -q --upgrade pip
.venv\Scripts\python.exe -m pip install -q -r requirements.txt

REM Start backend server in background
echo %GREEN%[INFO]%NC% Starting backend server on http://localhost:8000
start "Space Bio Backend" cmd /k "set PYTHONPATH=%CD% && .venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo %GREEN%[SUCCESS]%NC% Backend server starting...
timeout /t 5 /nobreak >nul
cd ..

REM Step 2: Start Frontend
echo.
echo %BLUE%=== Step 2: Starting Frontend Application ===%NC%
cd Frontend

REM Check if node_modules exists
if not exist "node_modules\" (
    echo %YELLOW%[INFO]%NC% Installing frontend dependencies...
    call npm install
) else (
    echo %GREEN%[INFO]%NC% Dependencies already installed
)

REM Start frontend server
echo %GREEN%[INFO]%NC% Starting frontend server on http://localhost:4200
start "Space Bio Frontend" cmd /k "npm start"

cd ..

REM Summary
echo.
echo ========================================
echo  %GREEN%Application Started Successfully!%NC%
echo ========================================
echo.
echo %BLUE%Backend API:%NC%
echo   - API Server: http://localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo   - Health: http://localhost:8000/health
echo.
echo %BLUE%Frontend App:%NC%
echo   - Application: http://localhost:4200
echo.
echo %YELLOW%[INFO]%NC% Both servers are running in separate windows
echo %YELLOW%[INFO]%NC% Close those windows to stop the servers
echo.
echo Press any key to open the application in your browser...
pause >nul

REM Open browser
start http://localhost:4200

echo.
echo %GREEN%[SUCCESS]%NC% Application is running!
echo.
pause
