"""
AI Skill for Motivational Advice and Task Insights
Unique feature for Phase V to give the bot personality.
"""
import random
from typing import Dict, List

def get_motivational_quote() -> str:
    """Returns a random motivational quote with a focus on productivity."""
    quotes = [
        "The way to get started is to quit talking and begin doing. - Walt Disney",
        "Don't let yesterday take up too much of today. - Will Rogers",
        "You don't have to be great to start, but you have to start to be great. - Zig Ziglar",
        "Focus on being productive instead of busy. - Tim Ferriss",
        "Productivity is never an accident. It is always the result of a commitment to excellence. - Paul J. Meyer",
        "It's not that I'm so smart, it's just that I stay with problems longer. - Albert Einstein (Perfect for Debugging!)",
        "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill"
    ]
    return random.choice(quotes)

def analyze_workload(tasks: List[Dict]) -> str:
    """Analyzes the density of tasks and gives a proactive advice."""
    pending = [t for t in tasks if not t.get('completed', False)]
    high_priority = [t for t in pending if t.get('priority') == 'high']
    
    if not pending:
        return "Your plate is clean! 🌟 Maybe it's time to learn something new or take a well-deserved break?"
    
    if len(high_priority) > 0:
        return f"You have {len(high_priority)} high-priority items staring at you. 🎯 I suggest tackling those first to clear your mind!"
    
    if len(pending) > 5:
        return "Whoa, your task list is getting a bit crowded! 📦 Try breaking these down into smaller steps."
    
    return "You're in a good flow. Keep that momentum going! 🚀"

def get_smart_insight(user_name: str, tasks: List[Dict]) -> str:
    """Combined smart insight for the AI to use."""
    quote = get_motivational_quote()
    analysis = analyze_workload(tasks)
    
    return f"Hey {user_name}! Here is your smart insight for today:\n\n{analysis}\n\n💡 Remember: {quote}"
