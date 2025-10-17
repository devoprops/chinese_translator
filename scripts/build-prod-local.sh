#!/bin/bash
# Build and Run Production Environment Locally
# Creates production Docker builds and runs them locally for testing

echo "🏭 Building Production Environment Locally"
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

# Create production .env files if they don't exist
echo "📝 Checking environment files..."

if [ ! -f "backend/.env.production" ]; then
    echo "Creating backend/.env.production..."
    cp backend/.env.example backend/.env.production
    echo "⚠️  Please update backend/.env.production with production values"
fi

if [ ! -f "frontend/.env.production" ]; then
    echo "Creating frontend/.env.production..."
    cp frontend/.env.example frontend/.env.production
    echo "⚠️  Please update frontend/.env.production with production API URL"
fi

echo ""
echo "🧹 Cleaning up old containers and images..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml down --remove-orphans

echo ""
echo "🏗️  Building production Docker images..."
echo "This may take several minutes..."
echo ""

# Build production images
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build --no-cache

echo ""
echo "✅ Build complete!"
echo ""
echo "🚀 Starting production containers..."

# Start production containers
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up

echo ""
echo "🛑 Containers stopped"
echo ""
echo "💡 To run in detached mode, use:"
echo "   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d"

