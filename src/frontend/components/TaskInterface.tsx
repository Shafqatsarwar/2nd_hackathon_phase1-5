"use client";

import { useState, useEffect, useCallback } from "react";

import { fetcher } from "../utils/fetcher";

interface Task {
    id: number;
    title: string;
    description: string;
    completed: boolean;
    priority: string;
    is_recurring: boolean;
    recurrence_interval: string | null;
    user_id: string;
}

interface TaskInterfaceProps {
    userId: string;
    token: string;
    title?: string;
}

export default function TaskInterface({ userId, token, title = "Evolution Task Matrix" }: TaskInterfaceProps) {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [newTitle, setNewTitle] = useState("");
    const [loading, setLoading] = useState(true);

    const fetchTasks = useCallback(async () => {
        try {
            const url = `/api/${userId}/tasks`;
            console.log("Fetching tasks from:", url); // Diagnostic
            const data = await fetcher(url, token);
            setTasks(data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    }, [userId, token]);

    useEffect(() => {
        fetchTasks();
    }, [fetchTasks]);

    const [priority, setPriority] = useState("medium");
    const [isRecurring, setIsRecurring] = useState(false);
    const [recurrenceInterval, setRecurrenceInterval] = useState("daily");

    const addTask = async () => {
        if (!newTitle) return;
        try {
            const res = await fetch(`/api/${userId}/tasks`, {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    title: newTitle,
                    description: "",
                    priority: priority,
                    is_recurring: isRecurring,
                    recurrence_interval: isRecurring ? recurrenceInterval : null
                })
            });
            if (res.ok) {
                const newTask = await res.json();
                setTasks([...tasks, newTask]);
                setNewTitle("");
                setPriority("medium");
                setIsRecurring(false);
                setRecurrenceInterval("daily");
            }
        } catch (err) {
            console.error(err);
        }
    };

    const toggleTask = async (id: number) => {
        try {
            const res = await fetch(`/api/${userId}/tasks/${id}/complete`, {
                method: "PATCH",
                headers: { Authorization: `Bearer ${token}` }
            });
            if (res.ok) {
                const updatedTask = await res.json();
                setTasks(tasks.map(t => t.id === id ? updatedTask : t));
            }
        } catch (err) {
            console.error(err);
        }
    };

    const deleteTask = async (id: number) => {
        try {
            const res = await fetch(`/api/${userId}/tasks/${id}`, {
                method: "DELETE",
                headers: { Authorization: `Bearer ${token}` }
            });
            if (res.ok) {
                setTasks(tasks.filter(t => t.id !== id));
            }
        } catch (err) {
            console.error(err);
        }
    };


    if (loading) return <div className="text-slate-500 py-10 text-center animate-pulse">Scanning matrix...</div>;

    return (
        <div className="w-full max-w-2xl mx-auto">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
                <span className="w-2 h-2 bg-purple-500 rounded-full animate-ping" />
                {title}
            </h2>

            <div className="bg-slate-900/50 border border-slate-800 rounded-3xl p-6 mb-8 shadow-2xl backdrop-blur-sm">
                <div className="flex flex-col gap-4">
                    <input
                        type="text"
                        value={newTitle}
                        onChange={(e) => setNewTitle(e.target.value)}
                        placeholder="Add to the evolution..."
                        className="bg-slate-950 border border-slate-800 rounded-xl px-5 py-3 text-white focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all placeholder:text-slate-600"
                    />
                    <div className="flex gap-3">
                        <select
                            value={priority}
                            onChange={(e) => setPriority(e.target.value)}
                            className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500 flex-1"
                        >
                            <option value="low">Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                        </select>

                        <div className="flex items-center gap-2 bg-slate-950 border border-slate-800 rounded-xl px-3">
                            <input
                                type="checkbox"
                                checked={isRecurring}
                                onChange={(e) => setIsRecurring(e.target.checked)}
                                className="w-4 h-4 accent-purple-500"
                                id="recurring-check"
                            />
                            <label htmlFor="recurring-check" className="text-sm text-slate-300 cursor-pointer select-none">Repeat</label>
                            {isRecurring && (
                                <select
                                    value={recurrenceInterval}
                                    onChange={(e) => setRecurrenceInterval(e.target.value)}
                                    className="bg-transparent text-sm text-purple-300 border-none focus:ring-0 cursor-pointer"
                                >
                                    <option value="daily">Daily</option>
                                    <option value="weekly">Weekly</option>
                                    <option value="monthly">Monthly</option>
                                </select>
                            )}
                        </div>

                        <button
                            onClick={addTask}
                            className="bg-white text-black font-bold px-6 rounded-xl hover:bg-neutral-200 transition-colors active:scale-95 cursor-pointer whitespace-nowrap"
                        >
                            Add
                        </button>
                    </div>
                </div>
            </div>

            <div className="space-y-3">
                {tasks.length === 0 ? (
                    <div className="text-center py-10 text-slate-600 border border-dashed border-slate-800 rounded-2xl">
                        No active evolution branches detected.
                    </div>
                ) : (
                    tasks.map(task => (
                        <div
                            key={task.id}
                            className={`flex flex-col p-4 bg-slate-900 border border-slate-800 rounded-xl transition hover:border-slate-600 group ${task.completed ? 'opacity-50' : ''}`}
                        >
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3 flex-1">
                                    <button
                                        onClick={() => toggleTask(task.id)}
                                        className={`w-5 h-5 rounded-md border flex items-center justify-center transition cursor-pointer ${task.completed ? 'bg-purple-600 border-purple-600' : 'border-slate-700 group-hover:border-purple-500'}`}
                                    >
                                        {task.completed && <span className="text-[10px] text-white">✓</span>}
                                    </button>
                                    <span
                                        onClick={() => toggleTask(task.id)}
                                        className={`transition cursor-pointer select-none flex-1 ${task.completed ? 'line-through text-slate-500' : 'text-slate-200'}`}
                                    >
                                        {task.title}
                                    </span>
                                </div>
                                <button
                                    onClick={() => deleteTask(task.id)}
                                    className="p-2 text-slate-600 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                                        <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                                    </svg>
                                </button>
                            </div>

                            {/* Priority and Recurrence Info */}
                            <div className="flex items-center gap-3 mt-2 text-xs">
                                <span className={`px-2 py-1 rounded-full ${
                                    task.priority === 'high' ? 'bg-red-500/20 text-red-400' :
                                    task.priority === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                                    'bg-green-500/20 text-green-400'
                                }`}>
                                    {task.priority}
                                </span>

                                {task.is_recurring && task.recurrence_interval && (
                                    <span className="px-2 py-1 rounded-full bg-blue-500/20 text-blue-400">
                                        Repeats: {task.recurrence_interval}
                                    </span>
                                )}

                                {task.is_recurring && !task.recurrence_interval && (
                                    <span className="px-2 py-1 rounded-full bg-blue-500/20 text-blue-400">
                                        Recurring
                                    </span>
                                )}
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}
