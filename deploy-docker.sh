#!/bin/bash

# Docker Deployment Script for Phase 1-4
# This script sets up and deploys the application using Docker

echo "🐳 Docker Deployment for Phase 1-4"
echo "=================================="
echo ""

# Step 1: Create .env file for Docker Compose
echo "📝 Step 1: Creating .env file for Docker Compose..."
cat > .env <<'EOF'
# Docker Compose Environment Variables
DATABASE_URL=postgresql://postgres:postgres@db:5432/todo_db
BETTER_AUTH_SECRET=your_better_auth_secret_here
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_token_here
GITHUB_OWNER=your_github_owner
GITHUB_REPO=your_github_repo
EOF

echo "✅ Created .env file"
echo ""

# Step 2: Stop any existing containers
echo "🛑 Step 2: Stopping any existing containers..."
echo "Running 'docker compose down'..."
docker compose down --remove-orphans || docker-compose down --remove-orphans || true
echo "✅ Containers stopped"
echo ""

# Step 3: Build Docker images
echo "🔨 Step 3: Building Docker images..."
echo "This may take 5-10 minutes on first build..."
echo ""

echo "Building backend image..."
docker build -f Dockerfile.backend -t todo-backend:latest . || {
    echo "❌ Backend build failed!"
    exit 1
}
echo "✅ Backend image built"
echo ""

echo "Building frontend image..."
docker build -f Dockerfile.frontend -t todo-frontend:latest . || {
    echo "❌ Frontend build failed!"
    exit 1
}
echo "✅ Frontend image built"
echo ""

# Step 4: Start containers
echo "🚀 Step 4: Starting containers..."
docker compose up -d || docker-compose up -d || {
    echo "❌ Failed to start containers!"
    exit 1
}
echo ""

# Step 5: Wait for services to be ready
echo "⏳ Step 5: Waiting for services to start..."
sleep 10
echo ""

# Step 6: Check container status
echo "📊 Step 6: Container Status"
echo "=========================="
docker-compose ps
echo ""

# Step 7: Show logs
echo "📜 Step 7: Recent Logs"
echo "===================="
docker-compose logs --tail=20
echo ""

# Step 8: Health checks
echo "🏥 Step 8: Health Checks"
echo "======================="
echo ""

echo "Testing backend health..."
curl -s http://localhost:8000/health | jq '.' 2>/dev/null || curl -s http://localhost:8000/health || echo "Backend not ready yet"
echo ""

echo "Testing frontend..."
curl -s -o /dev/null -w "Frontend HTTP Status: %{http_code}\n" http://localhost:3000 || echo "Frontend not ready yet"
echo ""

# Final instructions
echo "🎉 Deployment Complete!"
echo "======================"
echo ""
echo "Your application is now running in Docker:"
echo ""
echo "  🌐 Frontend:  http://localhost:3000"
echo "  🔧 Backend:   http://localhost:8000"
echo "  📚 API Docs:  http://localhost:8000/docs"
echo "  🗄️  Database: localhost:5432 (PostgreSQL)"
echo ""
echo "Useful commands:"
echo "  View logs:        docker-compose logs -f"
echo "  Stop containers:  docker-compose down"
echo "  Restart:          docker-compose restart"
echo "  Rebuild:          docker-compose up -d --build"
echo ""
echo "✨ Happy coding!"
