# Docker Development Script
# Starts both frontend and backend in Docker containers with hot-reload

Write-Host "[*] Starting Docker Development Environment" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "README.md")) {
    Write-Host "[!] Error: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

# Check if Docker is running
Write-Host "[i] Checking Docker..." -ForegroundColor Yellow
try {
    docker info | Out-Null
} catch {
    Write-Host "[!] Error: Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

Write-Host "[+] Docker is running" -ForegroundColor Green
Write-Host ""

# Create .env files if they don't exist
Write-Host "[i] Checking environment files..." -ForegroundColor Yellow

if (-not (Test-Path "backend\.env.local")) {
    Write-Host "Creating backend/.env.local..." -ForegroundColor Yellow
    Copy-Item "backend\.env.example" "backend\.env.local"
}

if (-not (Test-Path "frontend\.env.development")) {
    Write-Host "Creating frontend/.env.development..." -ForegroundColor Yellow
    Copy-Item "frontend\.env.example" "frontend\.env.development"
}

Write-Host ""
Write-Host "[+] Building and starting Docker containers..." -ForegroundColor Cyan
Write-Host "[i] This may take a few minutes on first run..." -ForegroundColor Yellow
Write-Host ""

# Start Docker Compose with development configuration
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

# Note: The above command runs in foreground. 
# Use Ctrl+C to stop the containers.

Write-Host ""
Write-Host "[*] Containers stopped" -ForegroundColor Yellow

