#!/bin/bash
# Local Development Script - No Docker
# Starts both frontend and backend in development mode with hot-reload

echo "🚀 Starting Local Development Environment"
echo "========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Check if ports are available
echo "🔍 Checking ports..."
if check_port 5000; then
    echo "⚠️  Warning: Port 5000 is already in use. Backend may fail to start."
fi
if check_port 3000; then
    echo "⚠️  Warning: Port 3000 is already in use. Frontend may fail to start."
fi

echo ""
echo "📦 Setting up Backend..."

# Backend setup
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Installing backend dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Copy .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local from .env.example..."
    cp .env.example .env.local
fi

# Start backend in background
echo "✅ Starting Flask backend on http://localhost:5000"
source venv/bin/activate && python main.py &
BACKEND_PID=$!

cd ..

echo ""
echo "📦 Setting up Frontend..."

# Frontend setup
cd frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Copy .env.development if it doesn't exist
if [ ! -f ".env.development" ]; then
    echo "Creating .env.development from .env.example..."
    cp .env.example .env.development
fi

# Start frontend in background
echo "✅ Starting React frontend on http://localhost:3000"
npm start &
FRONTEND_PID=$!

cd ..

echo ""
echo "✅ Development environment started!"
echo ""
echo "🌐 Access your application:"
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:5000"
echo "  Health:   http://localhost:5000/health"
echo ""
echo "💡 Tip: Both servers will auto-reload on file changes"
echo "📝 Press Ctrl+C to stop the servers"
echo ""
echo "Process IDs:"
echo "  Backend PID: $BACKEND_PID"
echo "  Frontend PID: $FRONTEND_PID"
echo ""

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait

