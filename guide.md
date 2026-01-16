# 📖 Developer Guide: The Evolution of Todo - Phase IV

Welcome to the internal developer guide for **Phase IV: Local Kubernetes Deployment**. This project implements a cloud-native, AI-powered Todo system using Spec-Driven Development (SDD).

 uv run uvicorn main:app --reload --port 8000
 
## 🎯 Phase IV Objectives

Phase IV proves the system is **cloud-native**, not just cloud-hosted. Key achievements:
- ✅ Dockerized frontend & backend with immutable containers
- ✅ Helm charts for declarative Kubernetes deployment
- ✅ Multi-replica readiness with zero data loss
- ✅ Local cluster deployment (Minikube/Docker Desktop)
- ✅ Enhanced AI chatbot with stateful voice features using **Vercel AI SDK**


## 🏗️ System Architecture

The application is split into three main tiers:

1. **Frontend (Next.js 15+)**: Modern React application using App Router, Tailwind CSS, Vercel AI SDK, and enhanced voice features
2. **Backend (FastAPI)**: High-performance Python service managing tasks, MCP integration, and AI orchestration
3. **Database (Neon PostgreSQL)**: Serverless PostgreSQL managed via SQLModel ORM

## 📂 Project Structure

```text
.
├── src/
│   ├── frontend/              # Next.js Application
│   │   ├── app/               # Routes and API Handlers
│   │   │   ├── chat/          # Enhanced AI Chat with Voice
│   │   │   ├── dashboard/     # Task Management Dashboard
│   │   │   └── api/           # API Routes (chat, auth)
│   │   ├── components/        # Reusable UI Components
│   │   ├── .env.local         # Frontend Environment Variables
│   │   └── package.json       # Frontend Dependencies
│   └── backend/               # FastAPI Application
│       ├── agents/            # OpenAI Orchestrator
│       ├── mcp_server/        # MCP Tools (GitHub, Web Search, Weather)
│       ├── models.py          # SQLModel Schemas
│       ├── main.py            # FastAPI Application Entry
│       ├── .env.local         # Backend Environment Variables
│       └── pyproject.toml     # Backend Dependencies
├── helm-chart/                # Kubernetes Manifests
│   ├── templates/             # K8s Resource Templates
│   ├── values.yaml            # Configuration Values
│   └── Chart.yaml             # Helm Chart Metadata
├── Dockerfile.backend         # Backend Container Spec
├── Dockerfile.frontend        # Frontend Container Spec
├── docker-compose.yml         # Local Docker Orchestration
├── requirements.txt           # Python Dependencies
├── package.json               # Root Package Configuration
└── README.md                  # Public Documentation
```

## 🎙️ Enhanced AI Chat & Voice Features

We use the **Vercel AI SDK** combined with **Web Speech API** for a seamless, stateful interactive experience.

### Key Features:
- **STT (Speech-to-Text)**: Native browser `SpeechRecognition` with real-time transcription
- **TTS (Text-to-Speech)**: Native browser `speechSynthesis` with auto-speak mode
- **Language Support**: 
  - English (`en-US`) - Default
  - Urdu (`ur-PK`) - Full RTL support
- **Stateful Voice Management**: 
  - Persistent voice state across sessions
  - Auto-speak toggle for AI responses
  - Language switching on-the-fly
  - Interim transcript display
- **Enhanced UX**:
  - Visual feedback for listening/speaking states
  - Error handling with user-friendly messages
  - Graceful degradation for unsupported browsers

### Voice State Interface:
```typescript
interface VoiceState {
  isListening: boolean;    // Microphone active
  isSpeaking: boolean;     // TTS active
  language: "en-US" | "ur-PK";  // Current language
  autoSpeak: boolean;      // Auto-read AI responses
  transcript: string;      // Current transcription
}
```

### How to Test Voice Features:
1. Start the dev servers (see Development Workflow below)
2. Navigate to `/chat`
3. **Microphone Input**: Click 🎙️ icon to start voice input
4. **Auto-Speak**: Toggle 🔊 icon in header to enable/disable auto-reading of AI responses
5. **Language Switch**: Click 🌐 icon to switch between English and Urdu
6. **Manual TTS**: Hover over any message and click the speaker icon

## 🛠️ MCP (Model Context Protocol) Tools

The backend exposes several tools to the AI Agent:

### Task Management Tools:
- `create_task`: Create new todo items
- `list_tasks`: Retrieve user's tasks
- `update_task`: Modify existing tasks
- `delete_task`: Remove tasks

### GitHub Integration Tools:
- `create_github_issue`: Create issues in your repo
- `create_pull_request`: Generate PRs
- `list_repositories`: Browse your GitHub repos

### Utility Tools:
- `web_search`: Real-time information via DuckDuckGo
- `get_weather`: Current weather and forecasts

## 🤖 AI Agent Skills

The AI agents are equipped with specialized skills for Phase IV deployment:

- **Dockerization Skill**: Auto-generates optimized Dockerfiles
- **Helm Chart Skill**: Creates declarative K8s manifests
- **Minikube Setup Skill**: Configures local K8s environments
- **K8s Deployment Skill**: Validates multi-replica readiness
- **kubectl-ai & kagent**: Natural language cluster orchestration

## 🚀 Development Workflow

### 1. Prerequisites
Ensure you have the following installed:
- **Node.js** ≥ 20 LTS
- **Python** ≥ 3.12
- **uv** (Python package manager)
- **Docker Desktop** (with Kubernetes enabled) OR **Minikube**
- **Helm** ≥ 3.x
- **kubectl**

### 2. Clone & Install Dependencies

```bash
# Clone the repository
git clone https://github.com/Shafqatsarwar/2nd_hackathon-phase1-4.git
cd 2nd_hackathon-phase1-4

# Install root dependencies
npm install

# Install frontend dependencies
cd src/frontend
npm install
cd ../..

# Install backend dependencies
uv sync
```

### 3. Environment Configuration

#### Frontend (.env.local)
Create `src/frontend/.env.local`:
```env
NEXT_PUBLIC_BACKEND_URL=http://127.0.0.1:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=my_super_secure_hackathon_secret_key_2025
DATABASE_URL=postgresql://neondb_owner:npg_zhJvIP74aTle@ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_token_here
GITHUB_OWNER=Shafqatsarwar
GITHUB_REPO=2nd_hackathon-phase1-4
```

#### Backend (.env.local)
Create `src/backend/.env.local`:
```env
DATABASE_URL=postgresql://neondb_owner:npg_zhJvIP74aTle@ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
BETTER_AUTH_SECRET=my_super_secure_hackathon_secret_key_2025
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_token_here
GITHUB_OWNER=Shafqatsarwar
GITHUB_REPO=2nd_hackathon-phase1-4
```

### 4. Run Development Servers

```bash
# Terminal 1: Backend
uv run uvicorn src.backend.main:app --reload --port 8000

# Terminal 2: Frontend
npm run dev --workspace=src/frontend
```

Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔒 Security & Secret Management

We use a "local-first" security model to keep API keys safe:

1.  **Environment Files**:
    -   `.env`, `src/backend/.env.local`, `src/frontend/.env.local`
    -   These contain real API keys but are **strictly gitignored**.
    -   Developers must create these manually (or use setup scripts).

2.  **Deployment Scripts**:
    -   `deploy-docker.sh` is used for automated deployment.
    -   **Important**: To prevent accidental leakage of keys in this script, we use:
        ```bash
        git update-index --assume-unchanged deploy-docker.sh
        ```
    -   This allows developers to modify the script locally with real keys without Git seeing the changes.

## ☸️ Kubernetes & Docker Deployment

For automated Docker deployment:
```bash
./deploy-docker.sh
```

For full Kubernetes instructions, see **[instructions.md](./instructions.md)**.

# Build images
docker build -f Dockerfile.backend -t todo-backend:latest .
docker build -f Dockerfile.frontend -t todo-frontend:latest .

# Deploy to Kubernetes
cd helm-chart
helm install todo-app .

# Access via port-forward
kubectl port-forward svc/todo-app-frontend-service 3000:3000
kubectl port-forward svc/todo-app-backend-service 8000:8000
```

## 📜 Constitutional Alignment

This project strictly follows the **[Constitution](./.specify/memory/📜%20CONSTITUTION-Hackathon%20II%20-%20Full%20Todo%20Spec-Driven%20Development.md)**:

- **Golden Rule**: No manual code writing. All logic derived from specs
- **Statelessness**: Services designed for horizontal scaling
- **Cloud-Ready**: Everything containerized and K8s-ready
- **AI-Native**: AI agents are first-class citizens using MCP tools

## 🔧 Troubleshooting

### Voice Features Not Working
- Ensure you're using Chrome/Edge (best support)
- Check microphone permissions in browser settings
- Verify HTTPS (required for production voice features)

### Backend Connection Issues
- Verify `NEXT_PUBLIC_BACKEND_URL` matches backend port
- Check backend is running: `curl http://localhost:8000/health`
- Review CORS settings in `src/backend/main.py`

### Database Connection Errors
- Verify `DATABASE_URL` is correct in both `.env.local` files
- Check Neon PostgreSQL dashboard for connection limits
- Ensure SSL mode is enabled

## 📚 Additional Resources

- **[README.md](./README.md)**: Public-facing project overview
- **[instructions.md](./instructions.md)**: Kubernetes deployment guide
- **[Constitution](./.specify/memory/)**: Project governance rules
- **[Skills](./.claude/skills/)**: AI agent deployment skills

## 🎓 Learning Path

1. **Phase I**: In-memory console application
2. **Phase II**: Full-stack web application with auth
3. **Phase III**: AI-powered chatbot with MCP
4. **Phase IV**: Local Kubernetes deployment ← **You are here**
5. **Phase V**: Advanced cloud-native with Kafka + Dapr

---

**Built for Panaversity Hackathon II** — Pushing the boundaries of AI-native, spec-driven software development.

