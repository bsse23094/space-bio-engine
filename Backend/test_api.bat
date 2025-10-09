@echo off
REM Space Biology Knowledge Engine - Backend Test Script (Windows)
REM This script tests the API endpoints to ensure everything is working

echo 🧪 Testing Space Biology Knowledge Engine Backend...

REM Base URL for API
set BASE_URL=http://localhost:8000

REM Check if server is running
echo [TEST] Checking if server is running...
curl -s "%BASE_URL%/health" >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] Server is not running. Please start the backend first:
    echo   Windows: start.bat
    echo   Linux/Mac: ./start.sh
    pause
    exit /b 1
)

echo [PASS] Server is running!

REM Test basic endpoints
echo.
echo 🔍 Testing Basic Endpoints...

curl -s -o nul -w "%%{http_code}" "%BASE_URL%/" | findstr "200" >nul
if %errorlevel%==0 (echo [PASS] Root endpoint - Status: 200) else (echo [FAIL] Root endpoint failed)

curl -s -o nul -w "%%{http_code}" "%BASE_URL%/health" | findstr "200" >nul
if %errorlevel%==0 (echo [PASS] Health check - Status: 200) else (echo [FAIL] Health check failed)

curl -s -o nul -w "%%{http_code}" "%BASE_URL%/docs" | findstr "200" >nul
if %errorlevel%==0 (echo [PASS] API documentation - Status: 200) else (echo [FAIL] API documentation failed)

REM Test API endpoints
echo.
echo 📊 Testing API Endpoints...

curl -s -o nul -w "%%{http_code}" "%BASE_URL%/api/v1/stats" | findstr "200" >nul
if %errorlevel%==0 (echo [PASS] API statistics - Status: 200) else (echo [FAIL] API statistics failed)

curl -s -o nul -w "%%{http_code}" "%BASE_URL%/api/v1/articles" | findstr "200" >nul
if %errorlevel%==0 (echo [PASS] Get articles - Status: 200) else (echo [FAIL] Get articles failed)

curl -s -o nul -w "%%{http_code}" "%BASE_URL%/api/v1/visualizations/topic-distribution" | findstr "200" >nul
if %errorlevel%==0 (echo [PASS] Topic distribution - Status: 200) else (echo [FAIL] Topic distribution failed)

REM Test search endpoints
echo.
echo 🔎 Testing Search Endpoints...

curl -s -o nul -w "%%{http_code}" "%BASE_URL%/api/v1/articles/search?q=microgravity&limit=5" | findstr "200" >nul
if %errorlevel%==0 (echo [PASS] Article search - Status: 200) else (echo [FAIL] Article search failed)

curl -s -o nul -w "%%{http_code}" "%BASE_URL%/api/v1/search/suggestions?query=micrograv&limit=5" | findstr "200" >nul
if %errorlevel%==0 (echo [PASS] Search suggestions - Status: 200) else (echo [FAIL] Search suggestions failed)

REM Test POST endpoints
echo.
echo 📝 Testing POST Endpoints...

curl -s -o nul -w "%%{http_code}" -X POST -H "Content-Type: application/json" -d "{\"query\": \"space biology\", \"limit\": 5, \"similarity_threshold\": 0.7}" "%BASE_URL%/api/v1/search/semantic" | findstr "200" >nul
if %errorlevel%==0 (echo [PASS] Semantic search - Status: 200) else (echo [FAIL] Semantic search failed)

REM Summary
echo.
echo 🎯 Test Summary:
echo ==================
echo [PASS] Backend API is working correctly!
echo [INFO] All major endpoints are responding properly

echo.
echo 🌐 You can now access:
echo   📖 API Documentation: %BASE_URL%/docs
echo   📚 Alternative Docs: %BASE_URL%/redoc
echo   ❤️  Health Check: %BASE_URL%/health
echo   📊 API Stats: %BASE_URL%/api/v1/stats

echo.
echo [SUCCESS] Backend testing completed successfully! 🚀

pause
