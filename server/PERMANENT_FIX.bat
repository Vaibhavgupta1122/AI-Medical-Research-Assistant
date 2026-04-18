@echo off
title AI Medical Research - PERMANENT ONE-CLICK FIX
echo ========================================
echo   AI MEDICAL RESEARCH ASSISTANT
echo   COMPLETE SERVER SOLUTION
echo ========================================
echo.

REM Step 1: Complete system cleanup
echo [STEP 1] COMPLETE SYSTEM CLEANUP...
py kill_all_servers.py
timeout /t 2 /nobreak >nul

REM Step 2: Kill any remaining processes
echo [STEP 2] KILLING REMAINING PROCESSES...
taskkill /IM node.exe /F >nul 2>&1
timeout /t 1 /nobreak >nul

REM Step 3: Verify port is free
echo [STEP 3] VERIFYING PORT 5000...
netstat -ano | findstr :5000 >nul
if %ERRORLEVEL% equ 0 (
    echo ✅ Port 5000 is FREE
) else (
    echo ❌ Port 5000 is still OCCUPIED
    echo Killing remaining processes...
    for /f "tokens=5" %%a in ('netstat -ano ^| find ":5000" ^| find "LISTENING"') do (
        taskkill /f /pid %%a >nul 2>&1
    )
    timeout /t 2 /nobreak >nul
)

REM Step 4: Start server with error handling
echo [STEP 4] STARTING BACKEND SERVER...
echo.
cd /d "%~dp0"
npm start

if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ SERVER START FAILED!
    echo Trying alternative approach...
    echo.
    echo [ALTERNATIVE] Starting with direct node...
    node server.js
)

echo.
echo ========================================
echo   SERVER STARTUP COMPLETE
echo   Access your app at:
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:5000
echo ========================================
pause
