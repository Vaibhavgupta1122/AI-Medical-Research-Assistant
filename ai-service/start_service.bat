@echo off
echo Starting AI Medical Research Service...
echo.

REM Kill any existing processes on port 8000
echo Checking for existing processes on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do (
    echo Terminating process %%a
    taskkill /f /pid %%a
)

REM Wait for processes to terminate
timeout /t 3 /nobreak >nul

REM Start the AI service
echo Starting AI service on port 8000...
py -3.12 -m uvicorn simple_main:app --host 127.0.0.1 --port 8000 --reload

pause
