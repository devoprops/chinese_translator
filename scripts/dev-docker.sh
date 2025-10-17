#!/bin/bash
# Docker Development Script
# Starts both frontend and backend in Docker containers with hot-reload

echo "🐳 Starting Docker Development Environment"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if Docker is running
echo "🔍 Checking Docker..."
if ! docker info >/dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Create .env files if they don't exist
echo "📝 Checking environment files..."

if [ ! -f "backend/.env.local" ]; then
    echo "Creating backend/.env.local..."
    cp backend/.env.example backend/.env.local
fi

if [ ! -f "frontend/.env.development" ]; then
    echo "Creating frontend/.env.development..."
    cp frontend/.env.example frontend/.env.development
fi

echo ""
echo "🏗️  Building and starting Docker containers..."
echo "This may take a few minutes on first run..."
echo ""

# Start Docker Compose with development configuration
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

# Note: The above command runs in foreground. 
# Use Ctrl+C to stop the containers.

echo ""
echo "🛑 Containers stopped"

