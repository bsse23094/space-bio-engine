@echo off
REM Quick verification that the backend is working

echo 🚀 Space Biology Knowledge Engine Backend Status Check
echo =====================================================

echo.
echo 📍 Current Directory:
cd

echo.
echo 📁 Checking for required files:
if exist "app\main.py" (
    echo ✅ app\main.py found
) else (
    echo ❌ app\main.py missing
)

if exist "requirements.txt" (
    echo ✅ requirements.txt found
) else (
    echo ❌ requirements.txt missing
)

if exist "start.bat" (
    echo ✅ start.bat found
) else (
    echo ❌ start.bat missing
)

echo.
echo 🌐 Testing server connection:
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Server is running on port 8000
    echo.
    echo 🎉 Backend is ready! You can access:
    echo   📖 API Docs: http://localhost:8000/docs
    echo   ❤️  Health: http://localhost:8000/health
    echo   📊 Stats: http://localhost:8000/api/v1/stats
) else (
    echo ❌ Server not responding on port 8000
    echo.
    echo 🔧 To start the server:
    echo   1. Make sure you're in the Backend directory
    echo   2. Run: .\start.bat
    echo   3. Or manually: python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
)

echo.
pause
