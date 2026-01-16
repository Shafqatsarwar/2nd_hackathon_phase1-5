@echo off
echo 🔧 Setting up environment files for Phase 1-4...
echo.

REM Create frontend .env.local
(
echo # Frontend Environment Variables for Phase 1-4
echo NEXT_PUBLIC_BACKEND_URL=http://127.0.0.1:8000
echo NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
echo BETTER_AUTH_SECRET=my_super_secure_hackathon_secret_key_2025
echo DATABASE_URL=postgresql://neondb_owner:npg_zhJvIP74aTle@ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require^&channel_binding=require
echo.
echo # OpenAI API Key for AI Chatbot
echo OPENAI_API_KEY=your_openai_api_key_here
echo.
echo # GitHub Integration
echo GITHUB_TOKEN=your_github_token_here
echo GITHUB_OWNER=Shafqatsarwar
echo GITHUB_REPO=2nd_hackathon-phase1-4
) > src\frontend\.env.local

echo ✅ Created src\frontend\.env.local
echo.

REM Create backend .env.local
(
echo # Backend Environment Variables for Phase 1-4
echo DATABASE_URL=postgresql://neondb_owner:npg_zhJvIP74aTle@ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require^&channel_binding=require
echo BETTER_AUTH_SECRET=my_super_secure_hackathon_secret_key_2025
echo.
echo # OpenAI API Key for AI Chatbot
echo OPENAI_API_KEY=your_openai_api_key_here
echo.
echo # GitHub Integration
echo GITHUB_TOKEN=your_github_token_here
echo GITHUB_OWNER=Shafqatsarwar
echo GITHUB_REPO=2nd_hackathon-phase1-4
) > src\backend\.env.local

echo ✅ Created src\backend\.env.local
echo.
echo 🎉 Environment setup complete!
echo.
echo Next steps:
echo 1. Install frontend dependencies: cd src\frontend ^&^& npm install
echo 2. Install backend dependencies: uv sync
echo 3. Run backend: uv run uvicorn src.backend.main:app --reload --port 8000
echo 4. Run frontend: npm run dev --workspace=src/frontend
echo.
pause
