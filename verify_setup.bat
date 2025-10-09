@echo off
REM Quick Check Script for Space Biology Knowledge Engine

echo ========================================
echo  Space Biology Knowledge Engine
echo  System Verification
echo ========================================
echo.

REM Check Python
echo [CHECK] Python installation...
python --version >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Python is installed
    python --version
) else (
    echo [FAIL] Python is NOT installed
    echo Please install Python 3.8+ from https://python.org
)

echo.

REM Check Node.js
echo [CHECK] Node.js installation...
node --version >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Node.js is installed
    node --version
    npm --version
) else (
    echo [FAIL] Node.js is NOT installed
    echo Please install Node.js 16+ from https://nodejs.org
)

echo.

REM Check directories
echo [CHECK] Project structure...
if exist "Backend\" (
    echo [OK] Backend directory found
) else (
    echo [FAIL] Backend directory missing
)

if exist "Frontend\" (
    echo [OK] Frontend directory found
) else (
    echo [FAIL] Frontend directory missing
)

if exist "datasets\" (
    echo [OK] Datasets directory found
) else (
    echo [WARN] Datasets directory missing (optional)
)

echo.

REM Check data files
echo [CHECK] Data files...
if exist "datasets\sb_publications_clean.csv" (
    echo [OK] Publications data found
) else (
    echo [WARN] Publications data missing
)

if exist "datasets\topics.csv" (
    echo [OK] Topics data found
) else (
    echo [WARN] Topics data missing
)

echo.

REM Summary
echo ========================================
echo  Verification Complete!
echo ========================================
echo.
echo If all checks passed, you can run:
echo   start_app.bat
echo.
echo For manual setup:
echo   Backend:  cd Backend ^&^& start.bat
echo   Frontend: cd Frontend ^&^& npm start
echo.
pause
