#!/bin/bash

echo "🚀 Chinese Learning App Deployment Script"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Build frontend
echo "📦 Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Check if build was successful
if [ ! -d "frontend/build" ]; then
    echo "❌ Error: Frontend build failed"
    exit 1
fi

echo "✅ Frontend built successfully"

# Test backend
echo "🧪 Testing backend..."
cd backend
python -c "import sys; print(f'Python version: {sys.version}')"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Test Flask app
echo "🧪 Testing Flask app..."
python -c "
from main import create_app
app = create_app()
print('✅ Flask app created successfully')
"

cd ..

echo ""
echo "🎉 Deployment preparation complete!"
echo ""
echo "Next steps:"
echo "1. Backend: Deploy to Railway/Render/Heroku"
echo "2. Frontend: Deploy to Cloudflare Pages"
echo "3. Update environment variables"
echo ""
echo "For detailed instructions, see setup.md"



