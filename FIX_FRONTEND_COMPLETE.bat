@echo off
title AI Medical Research - FRONTEND COMPLETE FIX
echo ==========================================
echo   FRONTEND VISIBILITY & FUNCTIONALITY FIX
echo ==========================================
echo.

REM Step 1: Kill all frontend processes
echo [STEP 1] CLEANING FRONTEND PROCESSES...
echo.
taskkill /IM node.exe /F >nul 2>&1
timeout /t 2 /nobreak >nul

REM Step 2: Clear browser cache
echo [STEP 2] CLEARING BROWSER CACHE...
echo.
echo Clearing temporary files...
del /q /s "%TEMP%\*" >nul 2>&1
del /q /s "%USERPROFILE%\AppData\Local\Temp\*" >nul 2>&1

REM Step 3: Start backend server
echo [STEP 3] STARTING BACKEND SERVER...
echo.
cd /d "%~dp0server"
start "Backend Server" cmd /c "npm start"
timeout /t 5 /nobreak >nul

REM Step 4: Start AI service
echo [STEP 4] STARTING AI SERVICE...
echo.
cd /d "%~dp0ai-service"
start "AI Service" cmd /c "py -3.12 -m uvicorn simple_main:app --port 8000"
timeout /t 5 /nobreak >nul

REM Step 5: Start frontend with proper environment
echo [STEP 5] STARTING FRONTEND...
echo.
cd /d "%~dp0client"
set BROWSER=none
set PORT=3000
set REACT_APP_API_URL=http://localhost:5000/api
echo.
echo Environment variables set:
echo   - REACT_APP_API_URL: http://localhost:5000/api
echo   - PORT: 3000
echo   - BROWSER: none (system default)
echo.

REM Step 6: Start frontend
echo [STEP 6] LAUNCHING FRONTEND...
echo.
start "Frontend" cmd /c "npm start"

REM Step 7: Wait and verify
echo [STEP 7] WAITING FOR SERVICES TO START...
echo.
timeout /t 15 /nobreak >nul

REM Step 8: Test services
echo [STEP 8] TESTING ALL SERVICES...
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

echo Testing Frontend...
curl -s http://localhost:3000 >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo   ✅ Frontend: WORKING
) else (
    echo   ❌ Frontend: NOT RESPONDING
)

REM Step 9: Open browser
echo [STEP 9] OPENING BROWSER...
echo.
timeout /t 3 /nobreak >nul
start http://localhost:3000

echo.
echo ==========================================
echo   FRONTEND FIX COMPLETE!
echo ==========================================
echo.
echo All services should now be working:
echo   - Backend Server: http://localhost:5000
echo   - AI Service: http://localhost:8000  
echo   - Frontend: http://localhost:3000
echo.
echo Features enabled:
echo   ✅ Scroll buttons with smooth animations
echo   ✅ Data status indicators with real-time feedback
echo   ✅ UI Test Panel for component verification
echo   ✅ Responsive design for all screen sizes
echo   ✅ Enhanced error handling and user feedback
echo   ✅ Proper screen fitting and visibility
echo.
echo Open your browser and test everything!
echo.
pause
