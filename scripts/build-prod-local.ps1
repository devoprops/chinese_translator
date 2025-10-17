# Build and Run Production Environment Locally
# Creates production Docker builds and runs them locally for testing

Write-Host "[*] Building Production Environment Locally" -ForegroundColor Green
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

# Create production .env files if they don't exist
Write-Host "[i] Checking environment files..." -ForegroundColor Yellow

if (-not (Test-Path "backend\.env.production")) {
    Write-Host "Creating backend/.env.production..." -ForegroundColor Yellow
    Copy-Item "backend\.env.example" "backend\.env.production"
    Write-Host "[!] Please update backend/.env.production with production values" -ForegroundColor Yellow
}

if (-not (Test-Path "frontend\.env.production")) {
    Write-Host "Creating frontend/.env.production..." -ForegroundColor Yellow
    Copy-Item "frontend\.env.example" "frontend\.env.production"
    Write-Host "[!] Please update frontend/.env.production with production API URL" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[+] Cleaning up old containers and images..." -ForegroundColor Cyan
docker-compose -f docker-compose.yml -f docker-compose.prod.yml down --remove-orphans

Write-Host ""
Write-Host "[+] Building production Docker images..." -ForegroundColor Cyan
Write-Host "[i] This may take several minutes..." -ForegroundColor Yellow
Write-Host ""

# Build production images
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build --no-cache

Write-Host ""
Write-Host "[+] Build complete!" -ForegroundColor Green
Write-Host ""
Write-Host "[+] Starting production containers..." -ForegroundColor Cyan

# Start production containers
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up

Write-Host ""
Write-Host "[*] Containers stopped" -ForegroundColor Yellow
Write-Host ""
Write-Host "[i] To run in detached mode, use:" -ForegroundColor Cyan
Write-Host "    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d" -ForegroundColor White

