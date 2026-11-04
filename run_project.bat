@echo off
title E-Waste Project Starter
echo ========================================================
echo   Launching E-Waste Classification and Recycling System
echo ========================================================
echo.

:: 1. Start Backend
echo [1/2] Starting Backend (Flask on Port 5000)...
start "E-Waste Backend" cmd /k "cd /d %~dp0backend && .\venv313\Scripts\python.exe app.py"

:: Wait 4 seconds for backend to initialize
timeout /t 4 /nobreak >nul

:: 2. Start Frontend
echo [2/2] Starting Frontend (React on Port 5173)...
start "E-Waste Frontend" cmd /k "cd /d %~dp0frontend_upload\frontend && npm run dev"

:: Wait 3 seconds and open browser
timeout /t 3 /nobreak >nul
start http://localhost:5173/

echo.
echo ========================================================
echo   Done! Both servers are running.
echo   Web App opened at: http://localhost:5173/
echo ========================================================
