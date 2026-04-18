@echo off
title AI Medical Research - Simple Startup
echo ==========================================
echo   AI MEDICAL RESEARCH ASSISTANT
echo   Simple Startup with npm start
echo ==========================================
echo.

REM Start Backend Server
echo [1/3] Starting Backend Server...
cd /d "%~dp0server"
start "Backend Server" cmd /c "npm start"
echo Backend Server: http://localhost:5000
timeout /t 3 /nobreak >nul

REM Start AI Service
echo [2/3] Starting AI Service...
cd /d "%~dp0ai-service"
start "AI Service" cmd /c "py -3.12 -m uvicorn simple_main:app --port 8000"
echo AI Service: http://localhost:8000
timeout /t 3 /nobreak >nul

REM Start Frontend
echo [3/3] Starting Frontend...
cd /d "%~dp0client"
start "Frontend" cmd /c "npm start"
echo Frontend: http://localhost:3000
timeout /t 5 /nobreak >nul

echo.
echo ==========================================
echo   ALL SERVICES STARTED!
echo ==========================================
echo.
echo Access Points:
echo   - Frontend: http://localhost:3000
echo   - Backend:  http://localhost:5000
echo   - AI Service: http://localhost:8000
echo.
echo Opening browser...
start http://localhost:3000
echo.
pause
