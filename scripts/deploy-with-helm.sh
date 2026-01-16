#!/bin/bash
# Phase IV - Deploy to Kubernetes with Helm
# Based on: .claude/skills/deploy-to-kubernetes.skill.md

set -e  # Exit on error

echo "☸️  Phase IV: Deploying to Kubernetes with Helm"
echo "==============================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Get project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Check if Helm is installed
echo "📋 Step 1: Checking Helm installation..."
if ! command -v helm &> /dev/null; then
    echo -e "${RED}❌ Helm is not installed${NC}"
    echo "Please install Helm: https://helm.sh/docs/intro/install/"
    exit 1
fi
echo -e "${GREEN}✅ Helm is installed: $(helm version --short)${NC}"

# Check if kubectl is configured
echo ""
echo "📋 Step 2: Checking kubectl configuration..."
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}❌ kubectl is not configured or cluster is not running${NC}"
    echo "Please run: ./scripts/setup-minikube.sh"
    exit 1
fi
echo -e "${GREEN}✅ kubectl is configured${NC}"

# Check if images are built
echo ""
echo "📋 Step 3: Checking Docker images..."
if ! docker images | grep -q "todo-backend"; then
    echo -e "${RED}❌ Backend image not found${NC}"
    echo "Please run: ./scripts/build-docker-images.sh"
    exit 1
fi
if ! docker images | grep -q "todo-frontend"; then
    echo -e "${RED}❌ Frontend image not found${NC}"
    echo "Please run: ./scripts/build-docker-images.sh"
    exit 1
fi
echo -e "${GREEN}✅ Docker images found${NC}"

# Check if helm chart exists
echo ""
echo "📋 Step 4: Checking Helm chart..."
if [ ! -d "helm-chart" ]; then
    echo -e "${RED}❌ Helm chart directory not found${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Helm chart found${NC}"

# Create secrets (if needed)
echo ""
echo "🔐 Step 5: Creating Kubernetes secrets..."
echo "Enter your environment variables (or press Enter to skip):"
read -p "DATABASE_URL (press Enter to use default): " DATABASE_URL
read -p "OPENAI_API_KEY (press Enter to use default): " OPENAI_API_KEY
read -p "BETTER_AUTH_SECRET (press Enter to use default): " BETTER_AUTH_SECRET

# Use defaults from .env.local.example if not provided
if [ -z "$DATABASE_URL" ]; then
    DATABASE_URL="postgresql://neondb_owner:npg_zhJvIP74aTle@ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
fi
if [ -z "$OPENAI_API_KEY" ]; then
    OPENAI_API_KEY="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"
fi
if [ -z "$BETTER_AUTH_SECRET" ]; then
    BETTER_AUTH_SECRET="my_super_secure_hackathon_secret_key_2025"
fi

kubectl create secret generic todo-app-secrets \
    --from-literal=DATABASE_URL="$DATABASE_URL" \
    --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY" \
    --from-literal=BETTER_AUTH_SECRET="$BETTER_AUTH_SECRET" \
    --from-literal=GITHUB_TOKEN="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" \
    --from-literal=GITHUB_OWNER="Shafqatsarwar" \
    --from-literal=GITHUB_REPO="2nd_hackathon-phase1-4" \
    --namespace=todo-app \
    --dry-run=client -o yaml | kubectl apply -f -

echo -e "${GREEN}✅ Secrets created${NC}"

# Deploy with Helm
echo ""
echo "🚀 Step 6: Deploying with Helm..."
cd helm-chart

# Check if release exists
if helm list -n todo-app | grep -q "todo-app"; then
    echo -e "${YELLOW}⚠️  Release 'todo-app' already exists${NC}"
    read -p "Do you want to upgrade it? (Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        helm upgrade todo-app . --namespace=todo-app
        echo -e "${GREEN}✅ Helm release upgraded${NC}"
    fi
else
    helm install todo-app . --namespace=todo-app
    echo -e "${GREEN}✅ Helm release installed${NC}"
fi

cd ..

# Wait for pods to be ready
echo ""
echo "⏳ Step 7: Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=todo-app --namespace=todo-app --timeout=300s || true

# Display deployment status
echo ""
echo "📊 Deployment Status:"
echo "===================="
kubectl get all -n todo-app

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "🌐 Accessing the Application:"
echo "============================="
echo "  Frontend: kubectl port-forward -n todo-app svc/todo-app-frontend-service 3000:3000"
echo "  Backend:  kubectl port-forward -n todo-app svc/todo-app-backend-service 8000:8000"
echo ""
echo "📝 Useful Commands:"
echo "==================="
echo "  kubectl get pods -n todo-app           - List pods"
echo "  kubectl logs -n todo-app <pod-name>    - View pod logs"
echo "  kubectl describe pod -n todo-app <pod> - Describe pod"
echo "  helm list -n todo-app                  - List Helm releases"
echo "  helm uninstall todo-app -n todo-app    - Uninstall release"
echo ""
