@echo off
title AI Medical Research Server - Secure Startup
echo ========================================
echo   AI Medical Research Server
echo   Secure Port 5000 Startup
echo ========================================
echo.

REM Step 1: Run port security script
echo [STEP 1] Securing port 5000...
py ensure_port_free.py
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to secure port 5000!
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Port 5000 is secured!
echo.

REM Step 2: Start the server
echo [STEP 2] Starting server...
npm start

echo.
echo Server stopped. Port 5000 is now free again.
pause
