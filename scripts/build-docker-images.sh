#!/bin/bash
# Phase IV - Build Docker Images
# Based on: .claude/skills/dockerize-applications.skill.md

set -e  # Exit on error

echo "🐳 Phase IV: Building Docker Images"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Get project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "📂 Project root: $PROJECT_ROOT"
echo ""

# Check if Dockerfiles exist
echo "📋 Step 1: Checking Dockerfiles..."
if [ ! -f "Dockerfile.backend" ]; then
    echo -e "${RED}❌ Dockerfile.backend not found${NC}"
    exit 1
fi
if [ ! -f "Dockerfile.frontend" ]; then
    echo -e "${RED}❌ Dockerfile.frontend not found${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Dockerfiles found${NC}"

# Check if using Minikube
echo ""
echo "📋 Step 2: Checking Minikube status..."
if minikube status &> /dev/null; then
    echo -e "${GREEN}✅ Minikube is running${NC}"
    echo "🔧 Setting Docker environment to use Minikube's Docker daemon..."
    eval $(minikube docker-env)
    echo -e "${GREEN}✅ Docker environment configured for Minikube${NC}"
else
    echo -e "${YELLOW}⚠️  Minikube is not running${NC}"
    echo "Building images for local Docker daemon..."
fi

# Build backend image
echo ""
echo "🔨 Step 3: Building backend image..."
echo "Image: todo-backend:latest"
docker build -f Dockerfile.backend -t todo-backend:latest . \
    --build-arg BUILDKIT_INLINE_CACHE=1

echo -e "${GREEN}✅ Backend image built successfully${NC}"

# Build frontend image
echo ""
echo "🔨 Step 4: Building frontend image..."
echo "Image: todo-frontend:latest"
docker build -f Dockerfile.frontend -t todo-frontend:latest . \
    --build-arg BUILDKIT_INLINE_CACHE=1

echo -e "${GREEN}✅ Frontend image built successfully${NC}"

# List images
echo ""
echo "📊 Built Images:"
echo "================"
docker images | grep -E "todo-(backend|frontend)|REPOSITORY"

echo ""
echo -e "${GREEN}✅ All images built successfully!${NC}"
echo ""
echo "🎯 Next Steps:"
echo "=============="
echo "  1. Deploy to Kubernetes: ./scripts/deploy-with-helm.sh"
echo "  2. Or test locally: docker run -p 8000:8000 todo-backend:latest"
echo ""
