@echo off
REM Phase 5 Environment Setup Script
REM This script creates all required .env files for Phase 5

echo Setting up Phase 5 environment files...

REM Create frontend .env.local
echo Creating src/frontend/.env.local...
(
echo # Frontend Environment Variables
echo # Place this file at: src/frontend/.env.local
echo.
echo # Backend API URL
echo NEXT_PUBLIC_BACKEND_URL=http://127.0.0.1:8000
echo.
echo # Better Auth Configuration
echo NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
echo BETTER_AUTH_SECRET=my_super_secure_hackathon_secret_key_2025
echo.
echo # Database Connection
echo DATABASE_URL=postgresql://neondb_owner:npg_zhJvIP74aTle@ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require^&channel_binding=require
echo.
echo # OpenAI API Key for Phase III AI Chatbot
echo OPENAI_API_KEY=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
) > src\frontend\.env.local

REM Create backend .env.local
echo Creating src/backend/.env.local...
(
echo # Backend Environment Variables
echo # Place this file at: src/backend/.env.local
echo.
echo # Database Connection
echo DATABASE_URL=postgresql://neondb_owner:npg_zhJvIP74aTle@ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require^&channel_binding=require
echo.
echo # Better Auth Secret
echo BETTER_AUTH_SECRET=my_super_secure_hackathon_secret_key_2025
echo.
echo # OpenAI API Key for Phase III AI Chatbot
echo OPENAI_API_KEY=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
) > src\backend\.env.local

REM Create root .env for Docker Compose
echo Creating root .env...
(
echo # Root Environment Variables for Docker Compose and Local Development
echo.
echo # Database Connection
echo DATABASE_URL=postgresql://neondb_owner:npg_zhJvIP74aTle@ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require^&channel_binding=require
echo POSTGRES_URL=postgresql://neondb_owner:npg_zhJvIP74aTle@ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require^&channel_binding=require
echo.
echo # Better Auth Configuration
echo BETTER_AUTH_SECRET=my_super_secure_hackathon_secret_key_2025
echo NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
echo.
echo # Backend API URL
echo NEXT_PUBLIC_BACKEND_URL=http://127.0.0.1:8000
echo.
echo # OpenAI API Key
echo OPENAI_API_KEY=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
) > .env

REM Create .env.production for Vercel
echo Creating .env.production...
(
echo # Vercel Production Environment Variables
echo # These should be set in Vercel Dashboard
echo.
echo BETTER_AUTH_SECRET=my_super_secure_hackathon_secret_key_2025
echo NEXT_PUBLIC_BETTER_AUTH_URL=https://your-app.vercel.app
echo NEXT_PUBLIC_BACKEND_URL=https://your-backend.vercel.app
echo POSTGRES_URL=postgresql://neondb_owner:npg_zhJvIP74aTle@ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require^&channel_binding=require
echo DATABASE_URL=postgresql://neondb_owner:npg_zhJvIP74aTle@ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require^&channel_binding=require
echo OPENAI_API_KEY=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
) > .env.production

echo.
echo ✅ All environment files created successfully!
echo.
echo Files created:
echo   - src/frontend/.env.local
echo   - src/backend/.env.local
echo   - .env
echo   - .env.production
echo.
echo ⚠️  IMPORTANT: These files contain sensitive credentials and are in .gitignore
echo    Do NOT commit them to version control!
echo.
pause
