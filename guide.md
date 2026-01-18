# 🛠️ Main Developer Guide: 2nd_hackathon_phase1-5

This guide is your primary reference for commands, structure, and development workflows for the **2nd_hackathon_phase1-5** project.

## 🔑 Credentials & Hints
For the Auth System (BetterAuth):
- **Email Hint**: `kha***@hotmail.com`
- **Password Hint**: `Pass***123`
- **Note**: Since the database is fresh on Vercel, you might need to **Sign Up** again if your login fails.

## 📂 Project Structure
```text
.
├── backend/               # Legacy/Standalone Backend
├── frontend/              # Legacy/Standalone Frontend
├── src/
│   ├── backend/           # ACTIVE Backend (FastAPI)
│   └── frontend/          # ACTIVE Frontend (Next.js)
├── helm-chart/            # Kubernetes Deployment Config
├── dapr-components/       # Dapr State & Pub/Sub Config
├── api.md                 # API Key Locations Tracking
├── guide.md               # You are here
└── instructions.md        # Beginner's Infra Guide
```

## 🚀 Local Development Commands

### 🐍 Backend (FastAPI)
Install dependencies and run:
```powershell
cd src/backend
uv sync
uv run uvicorn main:app --reload --port 8000
```
- **Port**: 8000
- **Docs**: http://127.0.0.1:8000/docs

### ⚛️ Frontend (Next.js)
Install dependencies and run:
```powershell
cd src/frontend
npm install
npm run dev
```
- **Port**: 3000
- **URL**: http://localhost:3000

## 🧪 Testing Workflow

### 1. Localhost Test
Verify the frontend can talk to the backend. Check the `/chat` route and ensure voice/AI works.

### 2. Docker Test
Ensure your Docker Desktop is running. This tests if the app can run in an isolated container environment.
```powershell
./deploy-docker.sh
```
**Developer Docker Utilities:**
- **View Logs**: `docker-compose logs -f` (See real-time errors)
- **Restart Services**: `docker-compose restart`
- **Rebuild from Scratch**: `docker-compose up -d --build` (Use this if you change code)
- **Check Running Containers**: `docker ps`

### 3. Kubernetes Test
Deploy using Helm locally to simulate a production-grade cluster environment.
```powershell
helm upgrade --install todo-app ./helm-chart -f local-secrets.yaml
```
**Developer Kubernetes (kubectl) Utilities:**
- **Check Pod Status**: `kubectl get pods` (Look for "Running")
- **View Pod Logs**: `kubectl logs -f <pod_name>`
- **Restart Deployment**: `kubectl rollout restart deployment <deploy_name>`
- **Debug Inside Pod**: `kubectl exec -it <pod_name> -- /bin/bash`
- **Port Forwarding (Manual)**: `kubectl port-forward svc/<service_name> 8000:8000`

### 4. Cloud Deployment (Vercel CLI)
To deploy the frontend to Vercel via terminal:
```powershell
# Install Vercel CLI globally if not already installed
npm i -g vercel

# Navigate to frontend and deploy
cd src/frontend
vercel login
vercel
```
*Note: Follow the prompts to link the project and add environment variables through the Vercel dashboard for security.*

## 🔄 Updating Project State
- **Adding Keys**: Use the `api.md` to track where you add new secrets.
- **New Features**: Ensure SQLModel schemas in `models.py` are updated if database changes occur.
- **Frontend Paths**: Always use `NEXT_PUBLIC_BACKEND_URL` from `.env.local`.

## 📦 Dependency Management
- **Python**: Use `uv` for fast, reproducible environments.
- **Node**: Use `npm` (Workspaces are supported in the root `package.json`).

---
**Tip**: Always run `git status` before committing. Check `api.md` to ensure you haven't left keys in tracked files like `local-secrets.yaml`.
