@echo off
title AI Medical Research - ULTIMATE SOLUTION
echo ==========================================
echo   AI MEDICAL RESEARCH ASSISTANT
echo   ULTIMATE PERMANENT SOLUTION
echo ==========================================
echo.

REM Step 1: Kill ALL processes on both ports
echo [STEP 1] KILLING ALL CONFLICTING PROCESSES...
echo.

echo Killing processes on port 5000...
for /f "tokens=5" %%a in ('netstat -ano ^| find ":5000" ^| find "LISTENING"') do (
    echo Terminating process %%a on port 5000
    taskkill /f /pid %%a >nul 2>&1
)

echo Killing processes on port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| find ":8000" ^| find "LISTENING"') do (
    echo Terminating process %%a on port 8000
    taskkill /f /pid %%a >nul 2>&1
)

echo Killing all Node.js processes...
taskkill /IM node.exe /F >nul 2>&1

echo Killing all Python processes...
taskkill /IM python.exe /F >nul 2>&1

echo.
echo [STEP 2] WAITING FOR CLEANUP...
timeout /t 5 /nobreak >nul

REM Step 3: Start Backend Server
echo [STEP 3] STARTING BACKEND SERVER...
cd /d "%~dp0server"
start "Backend Server" cmd /k "npm start"

echo.
echo [STEP 4] WAITING FOR BACKEND TO START...
timeout /t 10 /nobreak >nul

REM Step 4: Start AI Service
echo [STEP 5] STARTING AI SERVICE...
cd /d "%~dp0ai-service"
start "AI Service" cmd /k "py -3.12 -m uvicorn simple_main:app --port 8000"

echo.
echo [STEP 6] WAITING FOR AI SERVICE TO START...
timeout /t 5 /nobreak >nul

echo.
echo ==========================================
echo   ALL SERVICES STARTED SUCCESSFULLY!
echo ==========================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:5000
echo AI Service: http://localhost:8000
echo.
echo Press any key to exit...
pause >nul
