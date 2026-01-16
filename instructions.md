# 🛠️ Dashboard & Deployment Instructions

This guide covers everything you need to know about deploying "The Evolution of Todo" using **Docker** (Phase 1-4) and **Kubernetes**.

---

## 🐳 Docker Deployment (Recommended)

We have created an **automated deployment script** that handles everything for you.

### Option 1: Automated Deployment (Easiest)

**1. Navigate to the project directory:**
```bash
cd ~/Projects/2nd_hackathon-phase1-4
```

**2. Make the script executable:**
```bash
chmod +x deploy-docker.sh
```

**3. Run the deployment script:**
```bash
./deploy-docker.sh
```

**This script will automatically:**
- Create the `.env` file with your secure keys
- Build Docker images for Backend and Frontend
- Stop any conflicting containers
- Start all services using `docker-compose`
- Perform health checks

**Once finished, access your app:**
- **Frontend UI:** [http://localhost:3000](http://localhost:3000)
- **Backend API:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Database:** `localhost:5432`

---

### Option 2: Manual Docker Deployment

If you prefer to run commands manually:

**1. Build Images:**
```bash
# Backend (2-3 min)
docker build -f Dockerfile.backend -t todo-backend:latest .

# Frontend (3-5 min)
docker build -f Dockerfile.frontend -t todo-frontend:latest .
```

**2. Create .env File:**
Ensure you have a `.env` file in the root directory with the following variables:
- `DATABASE_URL`
- `BETTER_AUTH_SECRET`
- `OPENAI_API_KEY`
- `GITHUB_TOKEN` (Optional)

**3. Start Services:**
```bash
docker-compose up -d
```

**4. View Logs:**
```bash
docker-compose logs -f
```

---

## ☸️ Kubernetes Deployment (Proven Defense Strategy)

Follow these **exact numbered commands** to deploy the application during your presentation.

### 1. Pre-Flight Check & Cleanup
Ensure Docker ports used by local dev are free.

```bash
docker-compose down
```

### 2. Install Helm (If missing)
If `helm` command is not found:

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### 3. Deploy Application
This uses the custom chart we built.

```bash
helm upgrade --install todo-app ./helm-chart -f local-secrets.yaml
```

### 4. Verify Pods
Check that pods are running.

```bash
kubectl get pods
```

*(If Backend is 0/1, wait 30 seconds. If stuck, run restart command below)*

### 5. Force Restart (Fix for Startup Timing)
If backend says `CrashLoopBackOff`, run this to fix it instantly:

```bash
kubectl rollout restart deployment todo-app-backend
```

### 6. Access Application (Port Forward)
Run these commands in separate terminals (or background) to open the tunnels:

```bash
# Terminal 1: Frontend -> http://localhost:3000
kubectl port-forward svc/todo-app-frontend-service 3000:3000 &

# Terminal 2: Backend -> http://localhost:8000
kubectl port-forward svc/todo-app-backend-service 8000:8000 &
```

### 🔓 Restoration Step (For Judges/Review)
To make the application work, you must restore the API keys in `deploy-docker.sh` and `local-secrets.yaml` if they were removed for the repo push.


---

## 🔎 Useful Commands

| Action | Command |
|--------|---------|
| **Stop Docker** | `docker-compose down` |
| **Restart Docker** | `docker-compose restart` |
| **Check Logs** | `docker-compose logs -f` |
| **K8s Status** | `kubectl get pods` |
| **Uninstall Helm** | `helm uninstall todo-app` |

---

## 🤖 AI Features

Once deployed, the following AI features will be active:
- **Smart Chatbot:** Ask questions about tasks, weather, or GitHub.
- **Task Analysis:** Auto-generates tags and priority suggestions.
- **Voice Mode:** Speak to your todo list (browser-supported).

Enjoy your cloud-native AI application! 🚀