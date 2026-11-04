Write-Host "🚀 Starting EcoSort AI Backend on http://localhost:5000 ..." -ForegroundColor Green
Set-Location -Path "$PSScriptRoot\backend"
& "$PSScriptRoot\backend\venv313\Scripts\python.exe" app.py
