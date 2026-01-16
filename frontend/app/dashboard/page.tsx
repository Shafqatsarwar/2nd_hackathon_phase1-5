"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { createAuthClient } from "better-auth/react";
import TaskInterface from "../../components/TaskInterface";
import Link from "next/link";
import SignOutButton from "../../components/SignOutButton";

const authClient = createAuthClient();

export default function DashboardPage() {
    const [session, setSession] = useState<any>(null);
    const router = useRouter();

    useEffect(() => {
        async function init() {
            // Check for admin/guest override
            const isAdmin = localStorage.getItem("admin_access") === "true";
            if (isAdmin) {
                setSession({
                    user: { id: "admin", name: "Admin User", email: "admin@example.com" },
                    token: "admin_token"
                });
                return;
            }

            // Check Better Auth Session
            const { data } = await authClient.getSession();
            if (!data) {
                router.push("/auth");
                return;
            }
            setSession(data);
        }
        init();
    }, [router]);

    if (!session) {
        return (
            <div className="min-h-screen bg-neutral-950 flex items-center justify-center">
                <div className="w-16 h-16 border-4 border-purple-500/20 border-t-purple-500 rounded-full animate-spin" />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-neutral-950 text-white font-sans selection:bg-purple-500/30">
            {/* Background */}
            <div className="fixed inset-0 pointer-events-none">
                <div className="absolute top-[-20%] right-[-10%] w-[600px] h-[600px] bg-purple-600/10 blur-[120px] rounded-full" />
                <div className="absolute bottom-[-10%] left-[-10%] w-[500px] h-[500px] bg-blue-600/10 blur-[120px] rounded-full" />
                <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20" />
            </div>

            <div className="relative z-10 max-w-5xl mx-auto px-6 py-10">
                {/* Header */}
                <header className="flex justify-between items-center mb-12">
                    <div className="flex flex-col">
                        <h1 className="text-3xl font-black tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-white to-neutral-400">
                            EVOLUTION DASHBOARD
                        </h1>
                        <p className="text-purple-400 text-sm font-medium tracking-widest uppercase mt-1">
                            {session.user.name} • Phase IV
                        </p>
                    </div>

                    <div className="flex items-center gap-6">
                        <Link
                            href="/chat"
                            className="text-sm font-bold text-slate-400 hover:text-white transition-colors"
                        >
                            AI CHAT
                        </Link>
                        <SignOutButton />
                    </div>
                </header>

                {/* Task Interface */}
                <TaskInterface
                    userId={session.user.id}
                    token={session.token || "admin_token"}
                    title="Your Evolution Workspace"
                />
            </div>
        </div>
    );
}
