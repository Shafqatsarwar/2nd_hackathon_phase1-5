#!/bin/bash
# Phase IV - Complete Deployment Pipeline
# Orchestrates all deployment steps

set -e  # Exit on error

echo "🚀 Phase IV: Complete Kubernetes Deployment Pipeline"
echo "====================================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}This script will:${NC}"
echo "  1. Setup Minikube cluster"
echo "  2. Build Docker images"
echo "  3. Deploy to Kubernetes with Helm"
echo ""
read -p "Continue? (Y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "Deployment cancelled"
    exit 0
fi

# Step 1: Setup Minikube
echo ""
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${BLUE}Step 1/3: Setting up Minikube${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
bash "$SCRIPT_DIR/setup-minikube.sh"

# Step 2: Build Docker images
echo ""
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${BLUE}Step 2/3: Building Docker images${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
bash "$SCRIPT_DIR/build-docker-images.sh"

# Step 3: Deploy with Helm
echo ""
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${BLUE}Step 3/3: Deploying with Helm${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
bash "$SCRIPT_DIR/deploy-with-helm.sh"

# Final status
echo ""
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Phase IV Deployment Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo ""
echo "📊 Quick Status Check:"
kubectl get all -n todo-app
echo ""
echo "🌐 Access the application:"
echo "  Run: kubectl port-forward -n todo-app svc/todo-app-frontend-service 3000:3000"
echo "  Then open: http://localhost:3000"
echo ""
