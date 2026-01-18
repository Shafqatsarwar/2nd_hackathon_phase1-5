"use client";

import { useState } from "react";
import { signIn, signUp } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Loader2 } from "lucide-react";

export default function AuthPage() {
    const [isLogin, setIsLogin] = useState(true);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [name, setName] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const router = useRouter();

    const [showSuccess, setShowSuccess] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        setShowSuccess(false);

        try {
            if (isLogin) {
                await signIn.email({
                    email,
                    password,
                }, {
                    onSuccess: () => {
                        router.push("/dashboard");
                    },
                    onError: (ctx: any) => {
                        const msg = ctx?.error?.message || ctx?.message || "Invalid credentials or server error.";
                        setError(msg);
                        setLoading(false);
                    }
                });
            } else {
                await signUp.email({
                    email,
                    password,
                    name,
                }, {
                    onSuccess: () => {
                        setIsLogin(true); // Switch to login
                        setLoading(false);
                        setShowSuccess(true);
                        setError("");
                    },
                    onError: (ctx: any) => {
                        const msg = ctx?.error?.message || ctx?.message || "Failed to create account.";
                        setError(msg);
                        setLoading(false);
                    }
                });
            }
        } catch (err: any) {
            console.error("Auth Error:", err);
            setError(err.message || "Network error. Please check your connection.");
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-neutral-950 flex items-center justify-center p-4 relative overflow-hidden">
            {/* Background Effects */}
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-500/20 blur-[120px] rounded-full mix-blend-screen" />
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-500/20 blur-[120px] rounded-full mix-blend-screen" />

            <div className="w-full max-w-md bg-neutral-900/50 border border-white/10 backdrop-blur-xl rounded-3xl p-8 shadow-2xl relative z-10">
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-black text-white mb-2 tracking-tight">
                        {isLogin ? "Welcome Back" : "Start Evolving"}
                    </h1>
                    <p className="text-neutral-400 text-sm">
                        {isLogin ? "Enter your credentials to access your vault." : "Create your account to unlock AI-powered productivity."}
                    </p>
                </div>

                {showSuccess && (
                    <div className="mb-6 p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-400 text-sm text-center font-bold">
                        ✅ Account created successfully! <br /> Please log in with your new credentials.
                    </div>
                )}

                {error && (
                    <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-sm text-center font-medium">
                        ⚠️ {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-5">
                    {!isLogin && (
                        <div className="space-y-2">
                            <label className="text-xs font-bold text-neutral-500 uppercase tracking-widest pl-1">Full Name</label>
                            <input
                                type="text"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                className="w-full bg-neutral-800/50 border border-white/5 rounded-xl px-4 py-3 text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition"
                                placeholder="John Doe"
                                required
                            />
                        </div>
                    )}

                    <div className="space-y-2">
                        <label className="text-xs font-bold text-neutral-500 uppercase tracking-widest pl-1">Email Address</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full bg-neutral-800/50 border border-white/5 rounded-xl px-4 py-3 text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition"
                            placeholder="you@example.com"
                            required
                        />
                    </div>

                    <div className="space-y-2">
                        <label className="text-xs font-bold text-neutral-500 uppercase tracking-widest pl-1">Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full bg-neutral-800/50 border border-white/5 rounded-xl px-4 py-3 text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition"
                            placeholder="••••••••"
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white font-bold py-4 rounded-xl shadow-lg hover:shadow-purple-500/25 active:scale-[0.98] transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                    >
                        {loading && <Loader2 className="w-4 h-4 animate-spin" />}
                        {isLogin ? "Sign In" : "Create Account"}
                    </button>
                </form>

                <div className="mt-8 pt-8 border-t border-white/5 text-center">
                    <p className="text-neutral-400 text-sm">
                        {isLogin ? "Don't have an account?" : "Already have an account?"}
                        <button
                            onClick={() => setIsLogin(!isLogin)}
                            className="ml-2 text-purple-400 hover:text-purple-300 font-bold hover:underline transition"
                        >
                            {isLogin ? "Sign Up" : "Log In"}
                        </button>
                    </p>
                </div>

                <div className="mt-6 text-center">
                    <Link href="/" className="text-xs text-neutral-600 hover:text-neutral-400 transition">
                        ← Back to Home
                    </Link>
                </div>
            </div>
        </div>
    );
}
