#!/bin/bash
# Phase IV - Setup Minikube for Local Kubernetes Deployment
# Based on: .claude/skills/setup-minikube.skill.md

set -e  # Exit on error

echo "🚀 Phase IV: Setting up Minikube for Local Kubernetes Deployment"
echo "================================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Minikube is installed
echo "📋 Step 1: Checking Minikube installation..."
if ! command -v minikube &> /dev/null; then
    echo -e "${RED}❌ Minikube is not installed${NC}"
    echo "Please install Minikube: https://minikube.sigs.k8s.io/docs/start/"
    exit 1
fi
echo -e "${GREEN}✅ Minikube is installed: $(minikube version --short)${NC}"

# Check if kubectl is installed
echo ""
echo "📋 Step 2: Checking kubectl installation..."
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl is not installed${NC}"
    echo "Please install kubectl: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi
echo -e "${GREEN}✅ kubectl is installed: $(kubectl version --client --short 2>/dev/null || echo 'kubectl installed')${NC}"

# Check if Minikube is running
echo ""
echo "📋 Step 3: Checking Minikube status..."
if minikube status &> /dev/null; then
    echo -e "${YELLOW}⚠️  Minikube is already running${NC}"
    read -p "Do you want to restart it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🔄 Stopping Minikube..."
        minikube stop
        echo "🗑️  Deleting existing cluster..."
        minikube delete
    else
        echo -e "${GREEN}✅ Using existing Minikube cluster${NC}"
        kubectl config use-context minikube
        echo ""
        echo "📊 Cluster Info:"
        kubectl cluster-info
        exit 0
    fi
fi

# Start Minikube
echo ""
echo "🚀 Step 4: Starting Minikube cluster..."
echo "Driver: docker"
echo "CPUs: 2"
echo "Memory: 4GB"
echo "Disk: 20GB"
echo ""

minikube start \
    --driver=docker \
    --cpus=2 \
    --memory=4096 \
    --disk-size=20g \
    --kubernetes-version=stable

echo -e "${GREEN}✅ Minikube cluster started successfully${NC}"

# Enable addons
echo ""
echo "📦 Step 5: Enabling useful addons..."
minikube addons enable metrics-server
minikube addons enable dashboard
echo -e "${GREEN}✅ Addons enabled${NC}"

# Set kubectl context
echo ""
echo "🔧 Step 6: Setting kubectl context..."
kubectl config use-context minikube
echo -e "${GREEN}✅ kubectl context set to minikube${NC}"

# Create namespace
echo ""
echo "📁 Step 7: Creating application namespace..."
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -
echo -e "${GREEN}✅ Namespace 'todo-app' created${NC}"

# Display cluster info
echo ""
echo "📊 Cluster Information:"
echo "======================"
kubectl cluster-info
echo ""
kubectl get nodes
echo ""

# Display useful commands
echo ""
echo -e "${GREEN}✅ Minikube setup complete!${NC}"
echo ""
echo "📝 Useful Commands:"
echo "==================="
echo "  minikube status              - Check cluster status"
echo "  minikube dashboard           - Open Kubernetes dashboard"
echo "  minikube stop                - Stop the cluster"
echo "  minikube delete              - Delete the cluster"
echo "  kubectl get pods -n todo-app - List pods in todo-app namespace"
echo "  kubectl get all -n todo-app  - List all resources in todo-app namespace"
echo ""
echo "🎯 Next Steps:"
echo "=============="
echo "  1. Build Docker images: ./scripts/build-docker-images.sh"
echo "  2. Deploy with Helm: ./scripts/deploy-with-helm.sh"
echo ""
