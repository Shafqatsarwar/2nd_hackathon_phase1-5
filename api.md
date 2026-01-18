# API & Secret Keys Management

This file tracks all locations where API keys and sensitive credentials are added. If the AI agent is unavailable, use this list to manually update or remove keys before committing to GitHub.

## 🔑 Active Keys
- **OpenAI API Key**: Used for the Phase III AI Chatbot and Phase V agents.

## 📂 Search & Replace Locations

### 1. Root Directory
- `.env`: Main environment file for local development.
- `.env.production`: Production environment variables (for Vercel/Cloud).
- `.gitignore`: Ensures secret files are not tracked by Git.
- `local-secrets.yaml`: Used for Dapr/Local Kubernetes secrets.

### 2. Backend Files
- `src/backend/.env.local`: Primary backend config.
- `backend/.env.local`: Secondary/Legacy backend config.
- `src/backend/main.py`: (Reference only) Loads keys.
- `src/backend/agents/orchestrator.py`: (Reference only) Uses keys.

### 3. Frontend Files
- `src/frontend/.env.local`: Primary frontend config.
- `frontend/.env.local`: Secondary/Legacy frontend config.

### 4. Infrastructure (Phase V)
- `helm-chart/values.yaml`: Placeholder for K8s deployment (Key should be passed via `--set`).

---

## 🛠 Manual Removal Guide

To quickly remove all keys before a commit, you can run these search patterns or check the files above:

1. **Search for OpenAI Keys**: `sk-proj-`
2. **Search for GitHub Tokens**: `ghp_`
3. **Regex for env files**: `OPENAI_API_KEY=.*`

> **Note**: Always check `.gitignore` includes `local-secrets.yaml` and any `.env.local` files.
