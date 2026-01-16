#!/bin/bash

# Setup script for environment variables
# This script creates .env.local files with the correct values

echo "🔧 Setting up environment files for Phase 1-4..."

# Create frontend .env.local
cat > src/frontend/.env.local <<'EOF'
# Frontend Environment Variables for Phase 1-4
NEXT_PUBLIC_BACKEND_URL=http://127.0.0.1:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=my_super_secure_hackathon_secret_key_2025
DATABASE_URL=postgresql://neondb_owner:npg_zhJvIP74aTle@ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require

# OpenAI API Key for AI Chatbot
OPENAI_API_KEY=your_openai_api_key_here

# GitHub Integration
GITHUB_TOKEN=your_github_token_here
GITHUB_OWNER=Shafqatsarwar
GITHUB_REPO=2nd_hackathon-phase1-4
EOF

echo "✅ Created src/frontend/.env.local"

# Create backend .env.local
cat > src/backend/.env.local <<'EOF'
# Backend Environment Variables for Phase 1-4
DATABASE_URL=postgresql://neondb_owner:npg_zhJvIP74aTle@ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
BETTER_AUTH_SECRET=my_super_secure_hackathon_secret_key_2025

# OpenAI API Key for AI Chatbot
OPENAI_API_KEY=your_openai_api_key_here

# GitHub Integration
GITHUB_TOKEN=your_github_token_here
GITHUB_OWNER=Shafqatsarwar
GITHUB_REPO=2nd_hackathon-phase1-4
EOF

echo "✅ Created src/backend/.env.local"

echo ""
echo "🎉 Environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Install frontend dependencies: cd src/frontend && npm install"
echo "2. Install backend dependencies: uv sync"
echo "3. Run backend: uv run uvicorn src.backend.main:app --reload --port 8000"
echo "4. Run frontend: npm run dev --workspace=src/frontend"
