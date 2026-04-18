@echo off
echo Starting Backend Server...
echo.

REM Kill any existing processes on port 5000
echo Checking for existing processes on port 5000...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5000" ^| find "LISTENING"') do (
    echo Terminating process %%a
    taskkill /f /pid %%a
)

REM Wait for processes to terminate
timeout /t 3 /nobreak >nul

REM Start the backend server
echo Starting backend server on port 5000...
npm start

pause
