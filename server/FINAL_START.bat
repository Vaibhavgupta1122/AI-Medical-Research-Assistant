@echo off
title AI Medical Research Server - FINAL SOLUTION
echo ========================================
echo   AI MEDICAL RESEARCH SERVER
echo   FINAL PORT 5000 SOLUTION
echo ========================================
echo.

REM Step 1: Complete cleanup
echo [STEP 1] COMPLETE PORT CLEANUP...
py kill_all_servers.py
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Port cleanup failed!
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Port 5000 is completely clean!
echo.

REM Step 2: Start server
echo [STEP 2] Starting your server...
echo.
npm start

echo.
echo Server stopped. Port 5000 is free again.
pause
