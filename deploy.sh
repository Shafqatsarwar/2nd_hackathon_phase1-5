#!/bin/bash

# 🚀 Quick Deploy Script for Docker & Kubernetes
# This script automates the deployment process

set -e  # Exit on error

echo "🚀 Todo App - Docker & Kubernetes Deployment"
echo "=============================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if running in WSL
if grep -qi microsoft /proc/version; then
    print_info "Running in WSL environment"
fi

# Main menu
echo "Select deployment option:"
echo "1) Docker Compose (Quick local testing)"
echo "2) Kubernetes with Minikube (Production-like)"
echo "3) Build Docker images only"
echo "4) Clean up everything"
echo "5) Exit"
echo ""
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        echo ""
        print_info "Starting Docker Compose deployment..."
        echo ""
        
        # Check if .env exists
        if [ ! -f .env ]; then
            print_warning ".env file not found. Creating template..."
            cat > .env << 'EOF'
DATABASE_URL=postgresql://postgres:postgres@db:5432/todo_db
BETTER_AUTH_SECRET=change-this-secret-in-production
OPENAI_API_KEY=your-openai-api-key-here
GITHUB_TOKEN=your-github-token-here
GITHUB_OWNER=your-github-username
GITHUB_REPO=your-repo-name
EOF
            print_warning "Please edit .env file with your actual credentials!"
            read -p "Press Enter after updating .env file..."
        fi
        
        # Build images
        print_info "Building Docker images..."
        docker build -f Dockerfile.backend -t todo-backend:latest .
        docker build -f Dockerfile.frontend -t todo-frontend:latest .
        print_success "Images built successfully"
        
        # Start services
        print_info "Starting services with Docker Compose..."
        docker-compose up -d
        
        # Wait for services to be ready
        print_info "Waiting for services to start..."
        sleep 10
        
        # Test backend
        print_info "Testing backend health..."
        if curl -s http://localhost:8000/health > /dev/null; then
            print_success "Backend is healthy!"
        else
            print_error "Backend health check failed"
        fi
        
        echo ""
        print_success "Deployment complete!"
        echo ""
        echo "Access your application:"
        echo "  Frontend: http://localhost:3000"
        echo "  Backend API: http://localhost:8000/docs"
        echo ""
        echo "View logs: docker-compose logs -f"
        echo "Stop services: docker-compose down"
        ;;
        
    2)
        echo ""
        print_info "Starting Kubernetes deployment with Minikube..."
        echo ""
        
        # Check if minikube is installed
        if ! command -v minikube &> /dev/null; then
            print_error "Minikube is not installed. Please install it first."
            exit 1
        fi
        
        # Check if kubectl is installed
        if ! command -v kubectl &> /dev/null; then
            print_error "kubectl is not installed. Please install it first."
            exit 1
        fi
        
        # Check if helm is installed
        if ! command -v helm &> /dev/null; then
            print_error "Helm is not installed. Please install it first."
            exit 1
        fi
        
        # Start Minikube
        print_info "Starting Minikube..."
        minikube start --driver=docker --cpus=4 --memory=8192
        print_success "Minikube started"
        
        # Configure Docker to use Minikube's daemon
        print_info "Configuring Docker to use Minikube's daemon..."
        eval $(minikube docker-env)
        
        # Build images in Minikube
        print_info "Building Docker images in Minikube..."
        docker build -f Dockerfile.backend -t todo-backend:latest .
        docker build -f Dockerfile.frontend -t todo-frontend:latest .
        print_success "Images built in Minikube"
        
        # Create secrets
        print_info "Creating Kubernetes secrets..."
        read -p "Enter OPENAI_API_KEY: " openai_key
        read -p "Enter GITHUB_TOKEN (optional, press Enter to skip): " github_token
        
        kubectl create secret generic todo-app-secrets \
            --from-literal=DATABASE_URL="postgresql://postgres:postgres@postgres-service:5432/todo_db" \
            --from-literal=BETTER_AUTH_SECRET="change-this-in-production" \
            --from-literal=OPENAI_API_KEY="$openai_key" \
            --from-literal=GITHUB_TOKEN="${github_token:-none}" \
            --from-literal=GITHUB_OWNER="your-username" \
            --from-literal=GITHUB_REPO="your-repo" \
            --dry-run=client -o yaml | kubectl apply -f -
        
        print_success "Secrets created"
        
        # Deploy with Helm
        print_info "Deploying with Helm..."
        helm upgrade --install todo-app ./helm-chart \
            --set backend.image.pullPolicy=IfNotPresent \
            --set frontend.image.pullPolicy=IfNotPresent
        
        print_success "Helm chart deployed"
        
        # Wait for pods to be ready
        print_info "Waiting for pods to be ready..."
        kubectl wait --for=condition=ready pod -l app=todo-backend --timeout=120s
        kubectl wait --for=condition=ready pod -l app=todo-frontend --timeout=120s
        
        print_success "All pods are ready!"
        
        # Show pod status
        echo ""
        kubectl get pods
        echo ""
        
        print_success "Deployment complete!"
        echo ""
        echo "To access your application, run in separate terminals:"
        echo "  Terminal 1: kubectl port-forward svc/todo-app-frontend-service 3000:3000"
        echo "  Terminal 2: kubectl port-forward svc/todo-app-backend-service 8000:8000"
        echo ""
        echo "Then access:"
        echo "  Frontend: http://localhost:3000"
        echo "  Backend API: http://localhost:8000/docs"
        echo ""
        echo "View logs:"
        echo "  kubectl logs -l app=todo-backend"
        echo "  kubectl logs -l app=todo-frontend"
        ;;
        
    3)
        echo ""
        print_info "Building Docker images only..."
        echo ""
        
        print_info "Building backend image..."
        docker build -f Dockerfile.backend -t todo-backend:latest .
        print_success "Backend image built"
        
        print_info "Building frontend image..."
        docker build -f Dockerfile.frontend -t todo-frontend:latest .
        print_success "Frontend image built"
        
        echo ""
        print_success "All images built successfully!"
        docker images | grep todo
        ;;
        
    4)
        echo ""
        print_warning "This will remove all Docker containers, images, and Kubernetes deployments!"
        read -p "Are you sure? (yes/no): " confirm
        
        if [ "$confirm" = "yes" ]; then
            print_info "Cleaning up Docker Compose..."
            docker-compose down -v 2>/dev/null || true
            
            print_info "Cleaning up Kubernetes..."
            helm uninstall todo-app 2>/dev/null || true
            kubectl delete secret todo-app-secrets 2>/dev/null || true
            
            print_info "Removing Docker images..."
            docker rmi todo-backend:latest 2>/dev/null || true
            docker rmi todo-frontend:latest 2>/dev/null || true
            
            print_info "Stopping Minikube..."
            minikube stop 2>/dev/null || true
            
            print_success "Cleanup complete!"
        else
            print_info "Cleanup cancelled"
        fi
        ;;
        
    5)
        print_info "Exiting..."
        exit 0
        ;;
        
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

echo ""
print_info "Done! 🎉"
