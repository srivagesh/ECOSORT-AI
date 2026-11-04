@echo off
title EcoSort AI Backend
echo Starting E-Waste ML Backend on http://localhost:5000 ...
cd /d "%~dp0backend"
"venv313\Scripts\python.exe" app.py
pause
