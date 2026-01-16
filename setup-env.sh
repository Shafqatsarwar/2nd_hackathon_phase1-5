#!/bin/bash

# Setup script for local development environment
# This creates the necessary .env.local files with your credentials

echo "🔧 Setting up local development environment..."

# Create frontend .env.local
echo "📝 Creating src/frontend/.env.local..."
cat > src/frontend/.env.local << 'EOF'
# Backend API URL
NEXT_PUBLIC_BACKEND_URL=http://127.0.0.1:8000

# Better Auth Configuration
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=my_super_secure_hackathon_secret_key_2025

# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://neondb_owner:npg_zhJvIP74aTle@ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require

# OpenAI API Key
OPENAI_API_KEY=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

# GitHub Integration
GITHUB_TOKEN=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
GITHUB_OWNER=Shafqatsarwar
GITHUB_REPO=2nd_hackathon-phase1-4
EOF

# Create backend .env.local
echo "📝 Creating src/backend/.env.local..."
cat > src/backend/.env.local << 'EOF'
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://neondb_owner:npg_zhJvIP74aTle@ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require

# Better Auth Secret (must match frontend)
BETTER_AUTH_SECRET=my_super_secure_hackathon_secret_key_2025

# OpenAI API Key
OPENAI_API_KEY=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

# GitHub Integration
GITHUB_TOKEN=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
GITHUB_OWNER=Shafqatsarwar
GITHUB_REPO=2nd_hackathon-phase1-4
EOF

echo "✅ Environment files created successfully!"
echo ""
echo "📦 Next steps:"
echo "1. Install dependencies: npm install && uv sync"
echo "2. Start backend: uv run uvicorn src.backend.main:app --reload --port 8000"
echo "3. Start frontend: npm run dev --workspace=src/frontend"
echo ""
echo "🎉 Happy coding!"
