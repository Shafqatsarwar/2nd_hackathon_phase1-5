import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

const getDatabaseConfig = () => {
    // Determine if we are in build/static generation phase
    // Better Auth must NOT attempt a real connection during build
    const isBuild =
        process.env.NEXT_PHASE === 'phase-production-build' ||
        process.env.CI === 'true' ||
        process.env.VERCEL === '1' ||
        process.env.BUILD_ID !== undefined ||
        process.env.NEXT_PUBLIC_VERCEL_ENV === 'preview' ||
        process.env.NEXT_PUBLIC_VERCEL_ENV === 'production' ||
        (!process.env.DATABASE_URL && process.env.NODE_ENV === 'production');

    if (isBuild || !process.env.DATABASE_URL) {
        console.log("🛠️ Auth: Using memory fallback for build/static phase");
        return {
            provider: "sqlite",
            url: ":memory:",
        };
    }

    const url = process.env.DATABASE_URL || "sqlite://todo.db"; // Default to local sqlite
    console.log("📡 Auth Configuration Check:");
    console.log("   - DATABASE_URL:", url);

    if (url.startsWith("postgres")) {
        return {
            provider: "postgres",
            url: url,
        };
    }

    const path = require("path");
    // Ensure we are looking for todo.db in the frontend root or project root
    const dbFileName = url.replace("sqlite://", "").replace("sqlite:", "");
    const absolutePath = path.resolve(process.cwd(), dbFileName);

    console.log("   - SQLite Absolute Path:", absolutePath);

    return {
        provider: "sqlite",
        url: absolutePath,
    };
};

export const auth = betterAuth({
    database: getDatabaseConfig(),
    emailAndPassword: {
        enabled: true
    },
    plugins: [
        jwt({
            jwt: {
                issuer: "todo-evolution",
                expiresIn: "7d"
            }
        })
    ]
});
