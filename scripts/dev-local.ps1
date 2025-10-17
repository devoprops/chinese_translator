# Local Development Script - No Docker
# Starts both frontend and backend in development mode with hot-reload

Write-Host "[*] Starting Local Development Environment" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "README.md")) {
    Write-Host "[!] Error: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

# Function to check if port is in use
function Test-Port {
    param($Port)
    $connection = Test-NetConnection -ComputerName localhost -Port $Port -WarningAction SilentlyContinue -InformationLevel Quiet
    return $connection
}

# Check if ports are available
Write-Host "[i] Checking ports..." -ForegroundColor Yellow
if (Test-Port 5000) {
    Write-Host "[!] Warning: Port 5000 is already in use. Backend may fail to start." -ForegroundColor Yellow
}
if (Test-Port 3000) {
    Write-Host "[!] Warning: Port 3000 is already in use. Frontend may fail to start." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[+] Setting up Backend..." -ForegroundColor Cyan

# Backend setup
Set-Location backend

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment and install dependencies
Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
pip install -r requirements.txt

# Copy .env.local if it doesn't exist
if (-not (Test-Path ".env.local")) {
    Write-Host "Creating .env.local from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env.local"
}

# Start backend in background
Write-Host "[+] Starting Flask backend on http://localhost:5000" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; & 'venv\Scripts\Activate.ps1'; python main.py"

Set-Location ..

Write-Host ""
Write-Host "[+] Setting up Frontend..." -ForegroundColor Cyan

# Frontend setup
Set-Location frontend

# Install dependencies if node_modules doesn't exist
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
    npm install
}

# Copy .env.development if it doesn't exist
if (-not (Test-Path ".env.development")) {
    Write-Host "Creating .env.development from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env.development"
}

# Start frontend in background
Write-Host "[+] Starting React frontend on http://localhost:3000" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; npm start"

Set-Location ..

Write-Host ""
Write-Host "[+] Development environment started!" -ForegroundColor Green
Write-Host ""
Write-Host ">>> Access your application:" -ForegroundColor Cyan
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "  Backend:  http://localhost:5000" -ForegroundColor White
Write-Host "  Health:   http://localhost:5000/health" -ForegroundColor White
Write-Host ""
Write-Host "[i] Tip: Both servers will auto-reload on file changes" -ForegroundColor Yellow
Write-Host "[i] Close the terminal windows to stop the servers" -ForegroundColor Yellow
Write-Host ""

