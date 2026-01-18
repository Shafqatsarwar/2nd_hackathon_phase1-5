import { sql } from "@vercel/postgres";
import dotenv from "dotenv";

// Load environment variables from .env if present
dotenv.config();

if (!process.env.POSTGRES_URL && !process.env.DATABASE_URL) {
    console.error("Error: POSTGRES_URL or DATABASE_URL environment variable is definition required.");
    process.exit(1);
}

// Map DATABASE_URL to POSTGRES_URL if needed by @vercel/postgres
if (!process.env.POSTGRES_URL && process.env.DATABASE_URL) {
    process.env.POSTGRES_URL = process.env.DATABASE_URL;
}

async function run() {
    console.log("Initializing Better Auth tables...");
    console.log(`Connecting to: ${process.env.POSTGRES_URL?.split('@')[1]}`); // Log only host part for safety

    try {
        await sql`
            CREATE TABLE IF NOT EXISTS "user" (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                "emailVerified" BOOLEAN NOT NULL DEFAULT FALSE,
                image TEXT,
                "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
                "updatedAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        `;

        await sql`
            CREATE TABLE IF NOT EXISTS "session" (
                id TEXT PRIMARY KEY,
                "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                token TEXT NOT NULL UNIQUE,
                "expiresAt" TIMESTAMPTZ NOT NULL,
                "ipAddress" TEXT,
                "userAgent" TEXT,
                "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
                "updatedAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        `;

        await sql`
            CREATE TABLE IF NOT EXISTS "account" (
                id TEXT PRIMARY KEY,
                "accountId" TEXT NOT NULL,
                "providerId" TEXT NOT NULL,
                "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                "accessToken" TEXT,
                "refreshToken" TEXT,
                "idToken" TEXT,
                "accessTokenExpiresAt" TIMESTAMPTZ,
                "refreshTokenExpiresAt" TIMESTAMPTZ,
                scope TEXT,
                password TEXT,
                "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
                "updatedAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        `;

        await sql`
            CREATE TABLE IF NOT EXISTS "verification" (
                id TEXT PRIMARY KEY,
                identifier TEXT NOT NULL,
                value TEXT NOT NULL,
                "expiresAt" TIMESTAMPTZ NOT NULL,
                "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
                "updatedAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        `;

        // Add indices for performance
        await sql`CREATE INDEX IF NOT EXISTS idx_session_user ON "session"("userId");`;
        await sql`CREATE INDEX IF NOT EXISTS idx_account_user ON "account"("userId");`;
        await sql`CREATE INDEX IF NOT EXISTS idx_verification_identifier ON "verification"(identifier);`;

        console.log("✅ Done verifying/initializing database tables.");
    } catch (error) {
        console.error("❌ Failed to initialize database:", error);
        process.exit(1);
    }
}

run();
