# 🛠️ Phase IV Deployment Scripts

This directory contains executable scripts for Phase IV - Local Kubernetes Deployment.

## 📋 Available Scripts

### 1. **setup-minikube.sh**
Sets up a local Kubernetes cluster using Minikube.

**What it does:**
- Checks Minikube and kubectl installation
- Starts Minikube cluster with appropriate resources
- Enables useful addons (metrics-server, dashboard)
- Creates application namespace
- Displays cluster information

**Usage:**
```bash
chmod +x scripts/setup-minikube.sh
./scripts/setup-minikube.sh
```

### 2. **build-docker-images.sh**
Builds Docker images for frontend and backend.

**What it does:**
- Checks for Dockerfiles
- Configures Docker to use Minikube's daemon (if Minikube is running)
- Builds backend image (todo-backend:latest)
- Builds frontend image (todo-frontend:latest)
- Lists built images

**Usage:**
```bash
chmod +x scripts/build-docker-images.sh
./scripts/build-docker-images.sh
```

### 3. **deploy-with-helm.sh**
Deploys the application to Kubernetes using Helm.

**What it does:**
- Checks Helm installation
- Verifies kubectl configuration
- Creates Kubernetes secrets for environment variables
- Installs/upgrades Helm release
- Waits for pods to be ready
- Displays deployment status

**Usage:**
```bash
chmod +x scripts/deploy-with-helm.sh
./scripts/deploy-with-helm.sh
```

### 4. **deploy-phase4.sh** ⭐ (Recommended)
Complete deployment pipeline - runs all steps in order.

**What it does:**
- Runs setup-minikube.sh
- Runs build-docker-images.sh
- Runs deploy-with-helm.sh
- Displays final status

**Usage:**
```bash
chmod +x scripts/deploy-phase4.sh
./scripts/deploy-phase4.sh
```

## 🚀 Quick Start

### Option A: Complete Deployment (Recommended)
```bash
# Make all scripts executable
chmod +x scripts/*.sh

# Run complete deployment
./scripts/deploy-phase4.sh
```

### Option B: Step-by-Step
```bash
# Step 1: Setup Minikube
./scripts/setup-minikube.sh

# Step 2: Build images
./scripts/build-docker-images.sh

# Step 3: Deploy
./scripts/deploy-with-helm.sh
```

## 📊 After Deployment

### Access the Application
```bash
# Frontend
kubectl port-forward -n todo-app svc/todo-app-frontend-service 3000:3000

# Backend
kubectl port-forward -n todo-app svc/todo-app-backend-service 8000:8000
```

Then open http://localhost:3000 in your browser.

### Useful Commands
```bash
# Check deployment status
kubectl get all -n todo-app

# View pod logs
kubectl logs -n todo-app <pod-name>

# Describe a pod
kubectl describe pod -n todo-app <pod-name>

# Open Kubernetes dashboard
minikube dashboard

# List Helm releases
helm list -n todo-app

# Uninstall application
helm uninstall todo-app -n todo-app
```

## 🔧 Troubleshooting

### Minikube won't start
```bash
# Delete and recreate
minikube delete
minikube start --driver=docker
```

### Images not found in Minikube
```bash
# Ensure you're using Minikube's Docker daemon
eval $(minikube docker-env)

# Rebuild images
./scripts/build-docker-images.sh
```

### Pods not starting
```bash
# Check pod status
kubectl get pods -n todo-app

# View pod logs
kubectl logs -n todo-app <pod-name>

# Describe pod for events
kubectl describe pod -n todo-app <pod-name>
```

### Port forwarding issues
```bash
# Kill existing port forwards
pkill -f "port-forward"

# Try again
kubectl port-forward -n todo-app svc/todo-app-frontend-service 3000:3000
```

## 📚 Based on Skills

These scripts are based on the following skills from `.claude/skills/`:
- `setup-minikube.skill.md`
- `dockerize-applications.skill.md`
- `deploy-to-kubernetes.skill.md`
- `create-helm-charts.skill.md`

## ✅ Phase IV Requirements

These scripts ensure compliance with Phase IV constitutional requirements:
- ✅ Containers are immutable
- ✅ Config via environment variables
- ✅ Infrastructure defined declaratively (Helm charts)
- ✅ No hardcoded service URLs
- ✅ No local filesystem dependencies
- ✅ Kubernetes is source of truth
- ✅ System survives pod restarts with zero data loss

## 🎯 Next Steps

After successful deployment:
1. Test all features in the deployed application
2. Verify multi-replica scaling
3. Test pod restart resilience
4. Validate data persistence
5. Document any issues or improvements

---

**Happy Deploying! 🚀**
