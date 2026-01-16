"use client";

import { useState, useRef, useEffect } from "react";
import { useChat, Message } from "ai/react";
import { createAuthClient } from "better-auth/react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import ReactMarkdown from "react-markdown";
import { AnimatePresence, motion } from "framer-motion";
import {
    Mic,
    MicOff,
    Send,
    Volume2,
    VolumeX,
    StopCircle,
    User as UserIcon,
    Bot as BotIcon,
    Languages,
    Sparkles
} from "lucide-react";
import clsx from "clsx";
import SignOutButton from "../../components/SignOutButton";

const authClient = createAuthClient();

// Voice state management
interface VoiceState {
    isListening: boolean;
    isSpeaking: boolean;
    language: "en-US" | "ur-PK";
    autoSpeak: boolean;
    transcript: string;
}

export default function ChatPage() {
    const [session, setSession] = useState<any>(null);
    const [voiceState, setVoiceState] = useState<VoiceState>({
        isListening: false,
        isSpeaking: false,
        language: "en-US",
        autoSpeak: false,
        transcript: ""
    });

    const router = useRouter();
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const recognitionRef = useRef<any>(null);
    const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);

    // Vercel AI SDK Hook with enhanced configuration
    const { messages, input, setInput, handleInputChange, handleSubmit, isLoading, stop } = useChat({
        api: "/api/chat",
        body: {
            userId: session?.user?.id,
            token: session?.token,
            language: voiceState.language,
        },
        onError: (err: Error) => {
            console.error("Chat error:", err);
        },
        onFinish: (message) => {
            // Auto-speak AI responses if enabled
            if (voiceState.autoSpeak && message.role === "assistant") {
                speakMessage(message.content);
            }
        }
    });

    // Auth Check
    useEffect(() => {
        async function init() {
            const isAdmin = localStorage.getItem("admin_access") === "true";
            if (isAdmin) {
                setSession({
                    user: { id: "admin", name: "Khan Sarwar", email: "admin@example.com" },
                    token: "admin_token"
                });
                return;
            }

            const { data } = await authClient.getSession();
            if (!data) {
                router.push("/auth");
                return;
            }
            setSession(data);
        }
        init();
    }, [router]);

    // Auto-scroll to bottom
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    // Cleanup on unmount
    useEffect(() => {
        return () => {
            if (recognitionRef.current) {
                recognitionRef.current.stop();
            }
            if (window.speechSynthesis) {
                window.speechSynthesis.cancel();
            }
        };
    }, []);

    // Enhanced Speech Recognition (STT)
    const toggleListening = () => {
        if (!("webkitSpeechRecognition" in window) && !("SpeechRecognition" in window)) {
            alert("Speech recognition is not supported in this browser. Try Chrome or Edge.");
            return;
        }

        if (voiceState.isListening) {
            recognitionRef.current?.stop();
            setVoiceState(prev => ({ ...prev, isListening: false }));
        } else {
            try {
                const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
                const recognition = new SpeechRecognition();

                recognition.continuous = false;
                recognition.interimResults = true;
                recognition.lang = voiceState.language;
                recognition.maxAlternatives = 1;

                recognition.onstart = () => {
                    setVoiceState(prev => ({ ...prev, isListening: true, transcript: "" }));
                };

                recognition.onend = () => {
                    setVoiceState(prev => ({ ...prev, isListening: false }));
                };

                recognition.onerror = (event: any) => {
                    console.error("Speech recognition error:", event.error);

                    if (event.error === "not-allowed") {
                        alert("Microphone access denied. Please allow microphone access in your browser settings.");
                    } else if (event.error === "audio-capture") {
                        alert("Could not access microphone. Please check if a microphone is connected.");
                    }

                    setVoiceState(prev => ({ ...prev, isListening: false }));
                };

                recognition.onresult = (event: any) => {
                    let finalTranscript = "";
                    let interimTranscript = "";

                    for (let i = event.resultIndex; i < event.results.length; i++) {
                        const transcript = event.results[i][0].transcript;
                        if (event.results[i].isFinal) {
                            finalTranscript += transcript + " ";
                        } else {
                            interimTranscript += transcript;
                        }
                    }

                    if (finalTranscript) {
                        setInput(prev => prev ? prev + " " + finalTranscript.trim() : finalTranscript.trim());
                        setVoiceState(prev => ({ ...prev, transcript: finalTranscript.trim() }));
                        recognition.stop();
                    } else if (interimTranscript) {
                        setVoiceState(prev => ({ ...prev, transcript: interimTranscript }));
                    }
                };

                recognitionRef.current = recognition;
                recognition.start();
            } catch (error) {
                console.error("Error initializing speech recognition:", error);
                alert("Failed to initialize speech recognition. Please check browser permissions.");
                setVoiceState(prev => ({ ...prev, isListening: false }));
            }
        }
    };

    // Enhanced Text-to-Speech (TTS)
    const speakMessage = (text: string) => {
        if (!("speechSynthesis" in window)) {
            console.warn("Text-to-speech is not supported in this browser.");
            return;
        }

        if (voiceState.isSpeaking) {
            window.speechSynthesis.cancel();
            setVoiceState(prev => ({ ...prev, isSpeaking: false }));
            return;
        }

        // Cancel any ongoing speech
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = voiceState.language;
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;

        utterance.onstart = () => {
            setVoiceState(prev => ({ ...prev, isSpeaking: true }));
        };

        utterance.onend = () => {
            setVoiceState(prev => ({ ...prev, isSpeaking: false }));
        };

        utterance.onerror = (event) => {
            console.error("Speech synthesis error:", event);
            setVoiceState(prev => ({ ...prev, isSpeaking: false }));
        };

        utteranceRef.current = utterance;
        window.speechSynthesis.speak(utterance);
    };

    // Toggle language
    const toggleLanguage = () => {
        setVoiceState(prev => ({
            ...prev,
            language: prev.language === "en-US" ? "ur-PK" : "en-US"
        }));
    };

    // Toggle auto-speak
    const toggleAutoSpeak = () => {
        setVoiceState(prev => ({ ...prev, autoSpeak: !prev.autoSpeak }));
    };

    if (!session) return (
        <div className="min-h-screen bg-neutral-950 flex items-center justify-center">
            <div className="w-16 h-16 border-4 border-purple-500/20 border-t-purple-500 rounded-full animate-spin" />
        </div>
    );

    return (
        <div className="min-h-screen bg-neutral-950 text-slate-200 font-sans relative overflow-hidden flex flex-col">
            {/* Background Effects */}
            <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-purple-600/10 blur-[150px] pointer-events-none" />
            <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-blue-600/10 blur-[150px] pointer-events-none" />

            {/* Header */}
            <header className="px-6 py-4 border-b border-white/5 bg-neutral-900/50 backdrop-blur-md sticky top-0 z-20 flex justify-between items-center">
                <div className="flex items-center gap-4">
                    <Link href="/dashboard" className="p-2 hover:bg-white/5 rounded-full transition">
                        Dashboard
                    </Link>
                    <div className="h-6 w-[1px] bg-white/10" />
                    <div>
                        <h1 className="font-bold text-white text-lg flex items-center gap-2">
                            <Sparkles className="w-5 h-5 text-purple-400" />
                            AI Assistant
                        </h1>
                        <p className="text-xs text-purple-400 font-medium tracking-wider">
                            VOICE ENABLED • {voiceState.language === "en-US" ? "ENGLISH" : "اردو"}
                        </p>
                    </div>
                </div>
                <div className="flex items-center gap-4">
                    {/* Language Toggle */}
                    <button
                        onClick={toggleLanguage}
                        className="p-2 hover:bg-white/5 rounded-full transition"
                        title={`Switch to ${voiceState.language === "en-US" ? "Urdu" : "English"}`}
                    >
                        <Languages className="w-5 h-5" />
                    </button>

                    {/* Auto-speak Toggle */}
                    <button
                        onClick={toggleAutoSpeak}
                        className={clsx(
                            "p-2 rounded-full transition",
                            voiceState.autoSpeak ? "bg-purple-500/20 text-purple-400" : "hover:bg-white/5"
                        )}
                        title={`Auto-speak: ${voiceState.autoSpeak ? "ON" : "OFF"}`}
                    >
                        {voiceState.autoSpeak ? <Volume2 className="w-5 h-5" /> : <VolumeX className="w-5 h-5" />}
                    </button>

                    <span className="hidden md:block text-sm text-slate-400">{session.user.name}</span>
                    <SignOutButton />
                </div>
            </header>

            {/* Chat Area */}
            <main className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 scroll-smooth">
                <div className="max-w-3xl mx-auto space-y-6">
                    {messages.length === 0 && (
                        <div className="text-center py-20 opacity-50">
                            <div className="w-20 h-20 bg-purple-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
                                <BotIcon className="w-10 h-10 text-purple-400" />
                            </div>
                            <h2 className="text-2xl font-bold text-white mb-2">How can I help you?</h2>
                            <p className="text-slate-400">Manage tasks, ask questions, or check GitHub issues.</p>
                            <p className="text-xs text-slate-500 mt-2">
                                🎙️ Click the microphone to speak • 🔊 Auto-speak is {voiceState.autoSpeak ? "ON" : "OFF"}
                            </p>
                        </div>
                    )}

                    <AnimatePresence mode="popLayout">
                        {messages.map((m: Message) => (
                            <motion.div
                                key={m.id}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, scale: 0.9 }}
                                className={clsx(
                                    "flex gap-4 items-start",
                                    m.role === "user" ? "flex-row-reverse" : "flex-row"
                                )}
                            >
                                <div className={clsx(
                                    "w-8 h-8 rounded-full flex items-center justify-center shrink-0",
                                    m.role === "user" ? "bg-purple-600" : "bg-slate-700"
                                )}>
                                    {m.role === "user" ? <UserIcon size={16} /> : <BotIcon size={16} />}
                                </div>

                                <div className={clsx(
                                    "group relative max-w-[80%] px-5 py-3 rounded-2xl text-sm md:text-base leading-relaxed animate-in fade-in zoom-in-95",
                                    m.role === "user"
                                        ? "bg-purple-600 text-white rounded-tr-none"
                                        : "bg-neutral-800 border border-white/10 text-slate-200 rounded-tl-none shadow-sm"
                                )}>
                                    <div className="prose prose-invert prose-p:my-1 prose-pre:bg-black/50 prose-pre:p-2 prose-pre:rounded-lg max-w-none">
                                        <ReactMarkdown>{m.content}</ReactMarkdown>
                                    </div>

                                    {/* Message Actions */}
                                    <div className={clsx(
                                        "absolute top-full mt-1 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity",
                                        m.role === "user" ? "right-0" : "left-0"
                                    )}>
                                        <button
                                            onClick={() => speakMessage(m.content)}
                                            className="p-1.5 text-slate-400 hover:text-white bg-black/20 rounded-full hover:bg-black/40"
                                            title="Read aloud"
                                        >
                                            {voiceState.isSpeaking ? <VolumeX size={12} /> : <Volume2 size={12} />}
                                        </button>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>

                    {isLoading && (
                        <div className="flex gap-4">
                            <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center shrink-0">
                                <BotIcon size={16} />
                            </div>
                            <div className="bg-neutral-800/50 px-5 py-4 rounded-2xl rounded-tl-none flex gap-1">
                                <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                                <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                                <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            </main>

            {/* Input Area */}
            <footer className="p-4 md:p-6 bg-neutral-900/80 backdrop-blur-lg border-t border-white/5">
                <div className="max-w-3xl mx-auto relative flex gap-3 items-end">
                    <button
                        onClick={stop}
                        disabled={!isLoading}
                        className={clsx(
                            "absolute -top-14 left-1/2 -translate-x-1/2 bg-neutral-800 text-white px-4 py-2 rounded-full text-xs font-medium border border-white/10 hover:bg-neutral-700 transition flex items-center gap-2",
                            isLoading ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4 pointer-events-none"
                        )}
                    >
                        <StopCircle size={14} /> Stop Generating
                    </button>

                    <form onSubmit={handleSubmit} className="flex-1 flex gap-2 w-full">
                        <div className="relative flex-1">
                            <input
                                value={input}
                                onChange={handleInputChange}
                                placeholder={
                                    voiceState.isListening
                                        ? `🎙️ Listening... ${voiceState.transcript}`
                                        : "Message AI..."
                                }
                                className={clsx(
                                    "w-full bg-neutral-800 border-2 rounded-2xl px-4 py-4 pr-12 focus:outline-none focus:ring-4 focus:ring-purple-500/20 transition-all",
                                    voiceState.isListening
                                        ? "border-red-500/50 animate-pulse placeholder:text-red-400"
                                        : "border-transparent focus:border-purple-500/50 text-white placeholder:text-slate-500"
                                )}
                            />

                            <div className="absolute right-2 top-1/2 -translate-y-1/2 flex gap-1">
                                <button
                                    type="button"
                                    onClick={toggleListening}
                                    className={clsx(
                                        "p-2 rounded-xl transition-all active:scale-95",
                                        voiceState.isListening
                                            ? "bg-red-500/20 text-red-400 animate-pulse"
                                            : "hover:bg-white/10 text-slate-400 hover:text-white"
                                    )}
                                    title="Voice Input"
                                >
                                    {voiceState.isListening ? <MicOff size={20} /> : <Mic size={20} />}
                                </button>
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={isLoading || !input.trim()}
                            className="bg-purple-600 hover:bg-purple-500 disabled:opacity-50 disabled:hover:bg-purple-600 text-white p-4 rounded-2xl transition-all shadow-lg shadow-purple-900/20 active:scale-95"
                        >
                            <Send size={20} />
                        </button>
                    </form>
                </div>
            </footer>
        </div>
    );
}
