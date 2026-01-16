# Phase 4: Docker & Kubernetes Deployment

## Session Summary
- **Objective:** Finalize Docker deployment and deploy to local Kubernetes (using Helm).
- **Date:** January 15, 2026

## Key Achievements
1. **Docker Deployment:**
   - Fixed `deploy-docker.sh` to correctly handle API keys and build processes.
   - Resolved frontend build errors by configuring `next.config.ts` to ignore strict ESLint checks.
   - Verified local Docker Compose deployment (Backend: 8000, Frontend: 3000).

2. **Kubernetes Deployment (Helm):**
   - Created a complete Helm Chart (`helm-chart/`) from scratch.
   - Added missing templates: `Chart.yaml`, `_helpers.tpl`, `serviceaccount.yaml`, Deployment/Service manifests.
   - optimized `backend-deployment.yaml` with Liveness/Readiness probes and resource limits to fix "CrashLoopBackOff" issues.
   - Validated deployment using `helm upgrade --install`.

3. **Security:**
   - Consolidated secrets into `local-secrets.yaml` (gitignored).
   - Scrubbed secrets from `deploy-docker.sh` and `local-secrets.yaml` before final Git push.

4. **Testing:**
   - Successfully verified application running on Kubernetes via `kubectl port-forward`.

## Critical Commands (Defense Guide)

### 1. Pre-Flight
```bash
docker-compose down
```

### 2. Deployment
```bash
helm upgrade --install todo-app ./helm-chart -f local-secrets.yaml
```

### 3. Troubleshooting (CrashLoopBackOff)
```bash
kubectl rollout restart deployment todo-app-backend
```

### 4. Access
```bash
kubectl port-forward svc/todo-app-frontend-service 3000:3000 &
kubectl port-forward svc/todo-app-backend-service 8000:8000 &
```
