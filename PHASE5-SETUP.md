# Phase 5 - Advanced Cloud-Native Deployment Setup Guide

## 🎯 Overview
This document provides the complete setup guide for Phase 5 of Hackathon II: Advanced Cloud-Native Deployment with Distributed Intelligence.

## 📋 Prerequisites Completed
✅ Phase 1-4 completed successfully  
✅ All source files copied from `public/2nd_hackathon-phase1-4/`  
✅ Environment variables configured  
✅ Dapr components configured  
✅ Helm charts ready  

## 🔧 Environment Setup

### 1. Environment Files Created
All environment files have been configured with the following credentials:

#### Frontend (.env.local)
- Location: `src/frontend/.env.local`
- Contains: Backend URL, Better Auth config, Database URL, OpenAI API Key

#### Backend (.env.local)
- Location: `src/backend/.env.local`
- Contains: Database URL, Better Auth Secret, OpenAI API Key

#### Root (.env)
- Location: `./.env`
- Contains: All environment variables for Docker Compose

#### Production (.env.production)
- Location: `./.env.production`
- Contains: Vercel production environment variables

### 2. Database Configuration
```
Database: Neon Serverless PostgreSQL
Connection String: postgresql://neondb_owner:npg_zhJvIP74aTle@ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

### 3. Authentication
```
Better Auth Secret: my_super_secure_hackathon_secret_key_2025
Frontend URL: http://localhost:3000
Backend URL: http://127.0.0.1:8000
```

### 4. OpenAI API
```
API Key: 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
```

## 🏗️ Phase 5 Architecture

### Event-Driven Components
1. **Kafka/Redpanda** - Event streaming platform
2. **Dapr Pub/Sub** - Event communication abstraction
3. **Dapr State Management** - Distributed state storage
4. **Dapr Jobs** - Scheduled task execution
5. **Dapr Secrets** - Secure credential management

### Services Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                        │
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌─────────────────────┐  │
│  │ Frontend │───▶│ Chat API │───▶│   Kafka Cluster     │  │
│  │ Service  │    │ + MCP    │    │  ┌──────────────┐   │  │
│  └──────────┘    │ Tools    │    │  │ task-events  │   │  │
│                  └────┬─────┘    │  │ reminders    │   │  │
│                       │          │  │ task-updates │   │  │
│                       │          └──┴──────────────┴───┘  │
│                       ▼                    │               │
│                  ┌─────────┐              │               │
│                  │ Neon DB │              ▼               │
│                  └─────────┘    ┌──────────────────┐      │
│                                 │ Notification     │      │
│                                 │ Service          │      │
│                                 └──────────────────┘      │
│                                 ┌──────────────────┐      │
│                                 │ Recurring Task   │      │
│                                 │ Service          │      │
│                                 └──────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Phase 5 Features to Implement

### Advanced Features
1. **Recurring Tasks**
   - Auto-reschedule repeating tasks
   - Configurable recurrence patterns (daily, weekly, monthly)
   - Event-driven task creation

2. **Due Dates & Reminders**
   - Set task deadlines with date/time
   - Browser/email notifications
   - Scheduled reminder events via Dapr Jobs

3. **Intermediate Features**
   - Priorities & Tags/Categories
   - Search & Filter capabilities
   - Sort tasks by various criteria

### Event-Driven Implementation

#### Kafka Topics
| Topic | Producer | Consumer | Purpose |
|-------|----------|----------|---------|
| `task-events` | Chat API (MCP Tools) | Recurring Task Service, Audit Service | All task CRUD operations |
| `reminders` | Chat API (when due date set) | Notification Service | Scheduled reminder triggers |
| `task-updates` | Chat API | WebSocket Service | Real-time client sync |

#### Event Schemas

**Task Event:**
```json
{
  "event_type": "created|updated|completed|deleted",
  "task_id": 123,
  "task_data": { /* full task object */ },
  "user_id": "user123",
  "timestamp": "2026-01-16T22:00:00Z"
}
```

**Reminder Event:**
```json
{
  "task_id": 123,
  "title": "Task title",
  "due_at": "2026-01-17T10:00:00Z",
  "remind_at": "2026-01-17T09:00:00Z",
  "user_id": "user123"
}
```

## 🚀 Deployment Strategy

### Part A: Local Deployment (Minikube)
1. Deploy Kafka using Strimzi operator
2. Configure Dapr on Minikube
3. Deploy services with Helm charts
4. Test event-driven features locally

### Part B: Cloud Deployment
**Recommended Platform: Oracle Cloud (Always Free)**
- 4 OCPUs, 24GB RAM - always free
- No credit card charges after trial
- Best for learning without time pressure

**Alternative Platforms:**
- **Azure (AKS)**: $200 credits for 30 days
- **Google Cloud (GKE)**: $300 credits for 90 days

### Kafka Options
**For Local (Minikube):**
- Redpanda (Docker) - Recommended ⭐
- Bitnami Kafka Helm Chart
- Strimzi Operator

**For Cloud:**
- Redpanda Cloud Serverless (Free tier) - Recommended ⭐
- Confluent Cloud ($400 credit)
- Self-hosted with Strimzi

## 📁 Project Structure

```
2nd_hackathon_phase1-5/
├── .specify/                    # Spec-Kit configuration
│   └── memory/
│       ├── Full-CONSTITUTION.md
│       └── Phase-V-Advanced-Cloud-Native-Deployment-CONSTITUTION.md
├── src/
│   ├── frontend/               # Next.js frontend
│   │   ├── .env.local         # Frontend environment variables
│   │   └── ...
│   └── backend/               # FastAPI backend
│       ├── .env.local         # Backend environment variables
│       ├── agents/            # OpenAI Agents SDK
│       ├── mcp_server/        # MCP tools
│       └── ...
├── dapr-components/           # Dapr component definitions
│   ├── pubsub.yaml           # Kafka Pub/Sub component
│   ├── statestore.yaml       # PostgreSQL state store
│   └── secrets.yaml          # Secret management
├── dapr-config/              # Dapr configuration
├── helm-chart/               # Kubernetes Helm charts
│   ├── templates/
│   └── values.yaml
├── scripts/                  # Deployment scripts
│   ├── setup-minikube.sh
│   ├── deploy-phase4.sh
│   └── deploy-with-helm.sh
├── specs/                    # Specifications
│   └── phase-v-spec.md
├── history/                  # Project history
│   ├── prompts/             # Prompt history records
│   ├── adr/                 # Architecture decision records
│   └── skills/              # Reusable agent skills
├── .env                     # Root environment variables
├── .env.production          # Production environment variables
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile.frontend      # Frontend Docker image
├── Dockerfile.backend       # Backend Docker image
└── PHASE5-SETUP.md         # This file
```

## 🔐 Security Notes

⚠️ **IMPORTANT**: All `.env` and `.env.local` files are in `.gitignore` and contain sensitive credentials:
- Database connection strings
- API keys (OpenAI)
- Authentication secrets
- **NEVER commit these files to version control!**

## 📝 Next Steps

### 1. Verify Environment Setup
```bash
# Run the environment setup script
.\setup-phase5-env.bat

# Verify files were created
ls src/frontend/.env.local
ls src/backend/.env.local
ls .env
```

### 2. Install Dependencies
```bash
# Frontend dependencies
cd src/frontend
npm install

# Backend dependencies
cd ../backend
pip install -r requirements.txt
# or using uv
uv pip install -r requirements.txt
```

### 3. Test Local Development
```bash
# Terminal 1: Start backend
cd src/backend
uvicorn main:app --reload --port 8000

# Terminal 2: Start frontend
cd src/frontend
npm run dev
```

### 4. Set Up Minikube
```bash
# Start Minikube
minikube start --cpus=4 --memory=8192

# Install Dapr on Minikube
dapr init -k

# Verify Dapr installation
dapr status -k
```

### 5. Deploy Kafka on Minikube
```bash
# Using Strimzi operator
kubectl create namespace kafka
kubectl apply -f https://strimzi.io/install/latest?namespace=kafka

# Deploy Kafka cluster (configuration in helm-chart/)
kubectl apply -f helm-chart/kafka-cluster.yaml
```

### 6. Deploy Application with Helm
```bash
# Deploy using Helm
./scripts/deploy-with-helm.sh

# Or manually
helm install todo-app ./helm-chart
```

## 🧪 Testing Phase 5 Features

### Test Recurring Tasks
```bash
# Create a recurring task via chatbot
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a recurring task to check emails every day at 9 AM"}'
```

### Test Reminders
```bash
# Set a reminder
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Remind me to call mom tomorrow at 3 PM"}'
```

### Verify Event Publishing
```bash
# Check Kafka topics
kubectl exec -it kafka-cluster-kafka-0 -n kafka -- \
  bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic task-events \
  --from-beginning
```

## 📚 Documentation References

- [Full Constitution](/.specify/memory/Full-CONSTITUTION.md)
- [Phase V Constitution](/.specify/memory/Phase-V-Advanced-Cloud-Native-Deployment-CONSTITUTION.md)
- [Requirements Document](/.specify/memory/Requirments_Hackathon II.md)
- [Dapr Documentation](https://docs.dapr.io/)
- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [Strimzi Documentation](https://strimzi.io/docs/)

## 🎓 Skills & History

### Skills Directory
Location: `history/skills/`
- Reusable agent skills for deployment
- Cloud-native blueprints
- Infrastructure automation patterns

### Prompts History
Location: `history/prompts/`
- All prompt history records
- Phase-specific prompts
- General development prompts

### Architecture Decision Records
Location: `history/adr/`
- Significant architectural decisions
- Technology choices and rationale
- Design patterns and tradeoffs

## ✅ Completion Checklist

- [x] Environment files created and configured
- [x] Source files copied from Phase 1-4
- [x] Dapr components configured
- [x] Helm charts ready
- [x] Scripts copied
- [ ] Dependencies installed
- [ ] Local development tested
- [ ] Minikube setup complete
- [ ] Kafka deployed
- [ ] Dapr initialized
- [ ] Application deployed with Helm
- [ ] Event-driven features implemented
- [ ] Recurring tasks working
- [ ] Reminders functional
- [ ] Cloud deployment complete
- [ ] CI/CD pipeline configured

## 🆘 Troubleshooting

### Environment Variables Not Loading
```bash
# Recreate environment files
.\setup-phase5-env.bat
```

### Dapr Not Working
```bash
# Reinitialize Dapr
dapr uninstall -k
dapr init -k
```

### Kafka Connection Issues
```bash
# Check Kafka pods
kubectl get pods -n kafka

# Check Kafka logs
kubectl logs -f kafka-cluster-kafka-0 -n kafka
```

### Database Connection Issues
```bash
# Test database connection
psql "postgresql://neondb_owner:npg_zhJvIP74aTle@ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require"
```

---

**Last Updated**: 2026-01-16  
**Phase**: 5 - Advanced Cloud-Native Deployment  
**Status**: Setup Complete - Ready for Implementation
