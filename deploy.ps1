Write-Host "🚀 Chinese Learning App - Deployment Preparation" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "This script prepares the application for production deployment." -ForegroundColor Yellow
Write-Host "Use this before deploying to Railway/Cloudflare or other platforms." -ForegroundColor Yellow
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "README.md")) {
    Write-Host "❌ Error: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

Write-Host "📋 Checking environment files..." -ForegroundColor Cyan

# Check backend environment files
if (-not (Test-Path "backend\.env.production")) {
    Write-Host "⚠️  Warning: backend/.env.production not found" -ForegroundColor Yellow
    Write-Host "   Creating from template..." -ForegroundColor Yellow
    Copy-Item "backend\.env.example" "backend\.env.production"
    Write-Host "   Please update backend/.env.production with production values!" -ForegroundColor Red
}

# Check frontend environment files
if (-not (Test-Path "frontend\.env.production")) {
    Write-Host "⚠️  Warning: frontend/.env.production not found" -ForegroundColor Yellow
    Write-Host "   Creating from template..." -ForegroundColor Yellow
    Copy-Item "frontend\.env.example" "frontend\.env.production"
    Write-Host "   Please update frontend/.env.production with production API URL!" -ForegroundColor Red
}

Write-Host ""
Write-Host "📦 Building Frontend..." -ForegroundColor Cyan
Set-Location frontend

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
npm install

# Build for production
Write-Host "Building production bundle..." -ForegroundColor Yellow
npm run build

Set-Location ..

# Check if build was successful
if (-not (Test-Path "frontend/build")) {
    Write-Host "❌ Error: Frontend build failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Frontend built successfully" -ForegroundColor Green

Write-Host ""
Write-Host "🧪 Testing Backend..." -ForegroundColor Cyan
Set-Location backend

Write-Host "Python version:" -ForegroundColor Yellow
python -c "import sys; print(f'  {sys.version}')"

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Installing dependencies..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
pip install -q -r requirements.txt

# Test Flask app
Write-Host "Testing Flask app..." -ForegroundColor Yellow
$testResult = python -c @"
import sys
try:
    from main import create_app
    app = create_app()
    print('✅ Flask app created successfully')
    sys.exit(0)
except Exception as e:
    print(f'❌ Error creating Flask app: {e}')
    sys.exit(1)
"@

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Backend test failed" -ForegroundColor Red
    Set-Location ..
    exit 1
}

Write-Host $testResult -ForegroundColor Green
Set-Location ..

Write-Host ""
Write-Host "✅ Deployment preparation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "📚 Next Steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "For REMOTE deployment:" -ForegroundColor Yellow
Write-Host "  1. Commit and push changes to GitHub" -ForegroundColor White
Write-Host "  2. Railway and Cloudflare will auto-deploy" -ForegroundColor White
Write-Host ""
Write-Host "For LOCAL testing:" -ForegroundColor Yellow
Write-Host "  • Development:  .\scripts\dev-local.ps1" -ForegroundColor White
Write-Host "  • With Docker:  .\scripts\dev-docker.ps1" -ForegroundColor White
Write-Host "  • Production:   .\scripts\build-prod-local.ps1" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions:" -ForegroundColor Yellow
Write-Host "  • Deployment Guide: DEPLOYMENT.md" -ForegroundColor White
Write-Host "  • README: README.md" -ForegroundColor White
Write-Host ""
Write-Host "Current Production URLs:" -ForegroundColor Yellow
Write-Host "  • Frontend: https://devocosm.com/chinese-study/" -ForegroundColor White
Write-Host "  • Backend:  https://chinese-study-production.up.railway.app" -ForegroundColor White
Write-Host ""



