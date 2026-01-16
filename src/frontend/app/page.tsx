import Link from "next/link";

const features = [
    {
        label: "Smart Priorities",
        description:
            "Tag each task with High/Medium/Low, trigger AI prompts, and keep focus on what really matters.",
        accent: "from-purple-500 to-pink-500",
    },
    {
        label: "Recursive Workflows",
        description:
            "Live recursion lets you schedule daily, weekly, or monthly repetitions that AI re-creates automatically.",
        accent: "from-sky-500 to-emerald-500",
    },
    {
        label: "Secure Vaults",
        description:
            "Better Auth + Neon encryption keep each vault private, auditable, and ready for multi-device use.",
        accent: "from-amber-500 to-rose-500",
    },
];

export default function Home() {
    return (
        <main className="min-h-screen bg-neutral-950 flex flex-col items-center justify-center relative overflow-hidden text-white">
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-500/40 blur-[160px] rounded-full mix-blur-screen" />
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-500/60 blur-[160px] rounded-full mix-blur-screen" />

            <div className="relative z-10 text-center px-6 py-12">
                <h1 className="text-7xl md:text-9xl font-black text-transparent bg-clip-text bg-gradient-to-b from-white to-neutral-500 mb-6 tracking-tight">
                    EVOLVE.
                </h1>

                <p className="max-w-xl mx-auto text-lg md:text-xl text-neutral-300 mb-10 font-medium leading-relaxed">
                    The most colorful evolution of your todo list yet—featuring AI-guided recursion,
                    neon gradients, and a secure, full-stack stack built with Next.js, FastAPI, and Neon.
                </p>

                <div className="flex flex-col md:flex-row gap-5 justify-center items-center mb-14">
                    <Link
                        href="/auth"
                        className="relative overflow-hidden rounded-2xl px-8 py-4 bg-gradient-to-br from-white to-gray-200 text-black font-bold text-sm uppercase tracking-[0.3em] transition-transform active:scale-95"
                    >
                        Start the Evolution
                        <span className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition duration-300" />
                    </Link>

                    <Link
                        href="/dashboard"
                        className="px-8 py-4 border border-cyan-400 text-cyan-300 font-bold rounded-2xl text-sm uppercase tracking-[0.3em] hover:border-cyan-300 active:scale-95 transition"
                    >
                        Dashboard
                    </Link>

                    <Link
                        href="/chat"
                        className="px-8 py-4 border border-purple-500 text-purple-300 font-bold rounded-2xl text-sm uppercase tracking-[0.3em] hover:border-purple-400 hover:text-purple-100 active:scale-95 transition"
                    >
                        AI Chat
                    </Link>
                </div>

                <div className="max-w-5xl mx-auto grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                    {features.map((feature) => (
                        <Link key={feature.label} href="/dashboard" className="group block">
                            <article
                                className="bg-white/5 border border-white/10 rounded-3xl p-6 backdrop-blur-xl shadow-2xl transition group-hover:border-white/30 group-hover:bg-white/10 h-full"
                            >
                                <div
                                    className={`inline-flex items-center justify-center w-12 h-12 rounded-2xl mb-4 bg-gradient-to-br ${feature.accent} text-white font-black text-lg group-hover:scale-110 transition-transform`}
                                >
                                    {feature.label
                                        .split(" ")
                                        .map((word) => word.charAt(0))
                                        .join("")
                                        .slice(0, 2)
                                        .toUpperCase()}
                                </div>
                                <h3 className="text-xl font-semibold mb-2 group-hover:text-white transition-colors">{feature.label}</h3>
                                <p className="text-sm text-slate-300 leading-relaxed">{feature.description}</p>
                            </article>
                        </Link>
                    ))}
                </div>

                <div className="mt-12 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                    <div className="flex flex-col gap-2">
                        <span className="text-lg font-semibold text-slate-200">Guest Access</span>
                        <p className="text-sm text-slate-400 max-w-xl">
                            Tap the glowing <strong>G</strong> badge anytime to spin up an ephemeral guest vault—no login,
                            all of the same task intelligence.
                        </p>
                    </div>
                    <button
                        className="w-16 h-16 bg-gradient-to-br from-sky-400 to-purple-500 text-white text-2xl font-black rounded-full shadow-2xl flex items-center justify-center ring-4 ring-sky-500/40 hover:scale-105 transition"
                        aria-label="Guest mode"
                    >
                        G
                    </button>
                </div>

                <div className="mt-8 flex gap-8 justify-center opacity-50">
                    <div className="flex flex-col items-center">
                        <span className="text-2xl font-bold text-white">FastAPI</span>
                        <span className="text-xs uppercase tracking-[0.6em] text-slate-500">Backend</span>
                    </div>
                    <div className="flex flex-col items-center">
                        <span className="text-2xl font-bold text-white">Neon</span>
                        <span className="text-xs uppercase tracking-[0.6em] text-slate-500">Database</span>
                    </div>
                    <div className="flex flex-col items-center">
                        <span className="text-2xl font-bold text-white">Better Auth</span>
                        <span className="text-xs uppercase tracking-[0.6em] text-slate-500">Auth</span>
                    </div>
                </div>
            </div>

            <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 pointer-events-none" />
        </main>
    );
}
