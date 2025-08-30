Write-Host "🚀 Chinese Learning App Deployment Script" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "README.md")) {
    Write-Host "❌ Error: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

# Build frontend
Write-Host "📦 Building frontend..." -ForegroundColor Yellow
Set-Location frontend
npm install
npm run build
Set-Location ..

# Check if build was successful
if (-not (Test-Path "frontend/build")) {
    Write-Host "❌ Error: Frontend build failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Frontend built successfully" -ForegroundColor Green

# Test backend
Write-Host "🧪 Testing backend..." -ForegroundColor Yellow
Set-Location backend
python -c "import sys; print(f'Python version: {sys.version}')"

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "📥 Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Test Flask app
Write-Host "🧪 Testing Flask app..." -ForegroundColor Yellow
python -c "
from main import create_app
app = create_app()
print('✅ Flask app created successfully')
"

Set-Location ..

Write-Host ""
Write-Host "🎉 Deployment preparation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Backend: Deploy to Railway/Render/Heroku" -ForegroundColor White
Write-Host "2. Frontend: Deploy to Cloudflare Pages" -ForegroundColor White
Write-Host "3. Update environment variables" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see setup.md" -ForegroundColor White



