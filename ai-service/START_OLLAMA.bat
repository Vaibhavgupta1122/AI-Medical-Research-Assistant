@echo off
title AI Medical Research - Ollama Integration
echo ==========================================
echo   AI MEDICAL RESEARCH WITH OLLAMA
echo ==========================================
echo.

REM Check if Ollama is installed
echo [1/4] Checking Ollama installation...
ollama --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Ollama is not installed or not in PATH
    echo Please install Ollama from: https://ollama.ai/
    echo.
    pause
    exit /b 1
)
echo Ollama is installed!

REM Check if Ollama is running
echo [2/4] Checking Ollama service...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Starting Ollama service...
    start "Ollama Service" cmd /c "ollama serve"
    echo Waiting for Ollama to start...
    timeout /t 10 /nobreak >nul
) else (
    echo Ollama service is already running!
)

REM Check if Mistral model is available
echo [3/4] Checking Mistral model...
curl -s http://localhost:11434/api/tags | findstr mistral >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Pulling Mistral model (this may take a few minutes)...
    ollama pull mistral
    echo Mistral model downloaded!
) else (
    echo Mistral model is available!
)

REM Start AI service
echo [4/4] Starting AI Medical Research Service...
echo.
echo Service will be available at:
echo   - AI Service: http://localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo   - Health Check: http://localhost:8000/health
echo   - Ollama Models: http://localhost:8000/ollama/models
echo.
echo Starting AI service...
cd /d "%~dp0"
py -3.12 -m uvicorn simple_main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo AI Service stopped.
pause
