import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import dotenv from "dotenv";

dotenv.config();

// Ensure DATABASE_URL is set
if (!process.env.DATABASE_URL) {
    console.error("❌ DATABASE_URL is missing!");
    process.exit(1);
}

const auth = betterAuth({
    database: {
        provider: "postgres",
        url: process.env.DATABASE_URL
    },
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

async function seedAdmin() {
    console.log("Creating Admin User...");
    const email = "khansarwar1@hotmail.com";
    const password = "Admin123";
    const name = "Khan Sarwar";

    try {
        const user = await auth.api.signUpEmail({
            body: {
                email,
                password,
                name
            }
        });

        if (user) {
            console.log("✅ Admin user created successfully!");
            console.log(`📧 Email: ${email}`);
            console.log(`🔑 Password: ${password}`);
        }
    } catch (error: any) {
        if (error.code === "P2002" || error.message?.includes("Unique constraint")) {
            console.log("⚠️ Admin user already exists (Email is taken).");
        } else {
            console.error("❌ Failed to create admin user:", error);
            // Log full error for debugging
            if (error.body) console.error(JSON.stringify(error.body, null, 2));
        }
    }
}

seedAdmin();
