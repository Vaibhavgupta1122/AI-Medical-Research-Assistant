@echo off
title AI Medical Research - Service Test
echo ==========================================
echo   TESTING ALL SERVICES
echo ==========================================
echo.

echo [1/4] Testing Backend Server...
curl -UseBasicParsing -s http://localhost:5000/api/health > backend_test.json
findstr /C:"status" backend_test.json >nul
if %ERRORLEVEL% equ 0 (
    echo   [OK] Backend Server: WORKING
) else (
    echo   [ERROR] Backend Server: NOT RESPONDING
)

echo [2/4] Testing AI Service...
curl -UseBasicParsing -s http://localhost:8000/health > ai_test.json
findstr /C:"healthy" ai_test.json >nul
if %ERRORLEVEL% equ 0 (
    echo   [OK] AI Service: WORKING
) else (
    echo   [ERROR] AI Service: NOT RESPONDING
)

echo [3/4] Testing Frontend...
curl -UseBasicParsing -s http://localhost:3000 > frontend_test.html
findstr /C:"DOCTYPE" frontend_test.html >nul
if %ERRORLEVEL% equ 0 (
    echo   [OK] Frontend: WORKING
) else (
    echo   [ERROR] Frontend: NOT RESPONDING
)

echo [4/4] Testing API Connection...
curl -UseBasicParsing -s -X POST http://localhost:5000/api/auth/register -H "Content-Type: application/json" -d "{\"email\":\"test@example.com\",\"password\":\"password123\",\"name\":\"Test User\"}" > api_test.json
findstr /C:"token" api_test.json >nul
if %ERRORLEVEL% equ 0 (
    echo   [OK] API Connection: WORKING
) else (
    echo   [ERROR] API Connection: FAILED
)

echo.
echo ==========================================
echo   TEST RESULTS
echo ==========================================
echo.

echo Backend Status:
type backend_test.json 2>nul

echo.
echo AI Service Status:
type ai_test.json 2>nul

echo.
echo Opening browser...
start http://localhost:3000

echo.
echo Check browser console (F12) for any errors
echo.
pause
del backend_test.json ai_test.json frontend_test.html api_test.json 2>nul
