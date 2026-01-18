# ☁️ Beginner's Cloud & Infra Guide: 2nd_hackathon_phase1-5

If you're new to Docker, Kubernetes, or Cloud deployment for **2nd_hackathon_phase1-5**, follow these simple guidelines.

## 🐳 1. Docker Basics
Think of Docker as a "box" that contains everything your app needs to run.

- **Check if Docker is running**: `docker v` or `docker ps`
- **Build a Docker image**: `docker build -t app-name .`
- **Run a container**: `docker run -p 3000:3000 app-name`
- **Stop everything**: `docker-compose down`

**Shortcut**: Just use `./deploy-docker.sh` to build and start everything automatically.

## ☸️ 2. Kubernetes (K8s) Basics
Kubernetes is the tool that manages many Docker "boxes" across multiple servers.

- **Pods**: Smallest unit (runs your container).
- **Services**: Makes your app reachable on a network.
- **Helm**: A "package manager" for Kubernetes. It simplifies complex deployments.

### How to deploy to K8s locally:
1. Enable Kubernetes in Docker Desktop.
2. Run: `helm install todo-app ./helm-chart -f local-secrets.yaml`
3. View your pods: `kubectl get pods`

## 🚀 3. Cloud Deployment (The "Big League")

### Vercel (Frontend)
Vercel is great for Next.js.
- **Option A (GitHub)**: Connect your repo to Vercel dashboard. It deploys every time you push.
- **Option B (Terminal)**: Use the command line.
  1. Run `npm i -g vercel` (if not installed).
  2. Run `vercel` in your project folder.
- **Important**: Add your `.env` variables in the Vercel Dashboard settings.

### Cloud Backend (Vercel/Neon/Azure)
- **Database**: We use **Neon PostgreSQL**. It's serverless and easy to scale.
- **FastAPI**: Can be deployed as a serverless function on Vercel or in a container on Azure/GCP.

## 🛡️ Important Safety Rules
1. **NEVER** push your API keys to GitHub.
2. If you see a file mentioned in `api.md`, check it twice before committing.
3. If `kubectl` or `docker` commands fail, check if the service is actually started on your computer.

---
*Follow these steps in order: Local -> Docker -> Cloud.*
🚀 Happy Deploying!