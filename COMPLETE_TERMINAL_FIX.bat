@echo off
title AI Medical Research - COMPLETE TERMINAL FIX
echo =================================================
echo   AI MEDICAL RESEARCH ASSISTANT
echo   COMPLETE TERMINAL PROBLEM SOLVER
echo =================================================
echo.

REM Step 1: Show current status
echo [STEP 1] CHECKING CURRENT STATUS...
echo.
echo Processes on port 5000:
netstat -ano | findstr :5000
echo.
echo Processes on port 8000:
netstat -ano | findstr :8000
echo.
echo Node.js processes:
tasklist | findstr node
echo.
echo Python processes:
tasklist | findstr python
echo.

REM Step 2: Kill ALL conflicting processes
echo [STEP 2] COMPLETE PROCESS CLEANUP...
echo.

echo Killing port 5000 processes...
for /f "tokens=5" %%a in ('netstat -ano ^| find ":5000" ^| find "LISTENING"') do (
    echo   - Killing process %%a on port 5000
    taskkill /f /pid %%a >nul 2>&1
)

echo Killing port 8000 processes...
for /f "tokens=5" %%a in ('netstat -ano ^| find ":8000" ^| find "LISTENING"') do (
    echo   - Killing process %%a on port 8000
    taskkill /f /pid %%a >nul 2>&1
)

echo Killing all Node.js processes...
taskkill /IM node.exe /F >nul 2>&1

echo Killing all Python processes...
taskkill /IM python.exe /F >nul 2>&1

REM Step 3: Wait for cleanup
echo.
echo [STEP 3] WAITING FOR CLEANUP...
timeout /t 5 /nobreak >nul

REM Step 4: Verify cleanup
echo [STEP 4] VERIFYING CLEANUP...
echo.
echo Checking port 5000:
netstat -ano | findstr :5000 >nul
if %ERRORLEVEL% equ 0 (
    echo   ❌ Port 5000 still occupied
) else (
    echo   ✅ Port 5000 is FREE
)

echo Checking port 8000:
netstat -ano | findstr :8000 >nul
if %ERRORLEVEL% equ 0 (
    echo   ❌ Port 8000 still occupied
) else (
    echo   ✅ Port 8000 is FREE
)

REM Step 5: Start services properly
echo.
echo [STEP 5] STARTING SERVICES PROPERLY...
echo.

echo Starting Backend Server (port 5000)...
cd /d "%~dp0server"
start "Backend Server" /min cmd /c "npm start"

echo Waiting for backend to start...
timeout /t 8 /nobreak >nul

echo Starting AI Service (port 8000)...
cd /d "%~dp0ai-service"
start "AI Service" /min cmd /c "py -3.12 -m uvicorn simple_main:app --port 8000"

echo Waiting for AI service to start...
timeout /t 5 /nobreak >nul

REM Step 6: Final verification
echo.
echo [STEP 6] FINAL VERIFICATION...
echo.

echo Testing Backend Server...
curl -s http://localhost:5000/api/health >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo   ✅ Backend Server: WORKING
) else (
    echo   ❌ Backend Server: NOT RESPONDING
)

echo Testing AI Service...
curl -s http://localhost:8000/health >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo   ✅ AI Service: WORKING
) else (
    echo   ❌ AI Service: NOT RESPONDING
)

echo.
echo =================================================
echo   COMPLETE TERMINAL FIX FINISHED
echo =================================================
echo.
echo Access Points:
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:5000
echo   AI Service: http://localhost:8000
echo.
echo All terminal problems should now be resolved!
echo Press any key to exit...
pause >nul
