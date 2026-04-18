@echo off
title AI Medical Research - Quick Fix
echo ==========================================
echo   QUICK ISSUE RESOLUTION
echo ==========================================
echo.

echo [1/5] KILLING ALL CONFLICTING PROCESSES...
taskkill /IM node.exe /F >nul 2>&1
taskkill /IM python.exe /F >nul 2>&1
timeout /t 3 /nobreak >nul

echo [2/5] CLEARING TEMP FILES...
del /q /s "%TEMP%\*" >nul 2>&1
timeout /t 2 /nobreak >nul

echo [3/5] STARTING BACKEND SERVER...
cd /d "%~dp0server"
start "Backend Server" cmd /c "npm start"
timeout /t 5 /nobreak >nul

echo [4/5] STARTING AI SERVICE...
cd /d "%~dp0ai-service"
start "AI Service" cmd /c "py -3.12 -m uvicorn simple_main:app --port 8000"
timeout /t 5 /nobreak >nul

echo [5/5] STARTING FRONTEND...
cd /d "%~dp0client"
start "Frontend" cmd /c "npm start"
timeout /t 10 /nobreak >nul

echo.
echo ==========================================
echo   ALL SERVICES STARTED!
echo ==========================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:5000
echo AI Service: http://localhost:8000
echo.
echo Opening browser...
start http://localhost:3000
echo.
pause
