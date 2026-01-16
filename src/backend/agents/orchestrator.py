"""
AI Agent Orchestrator for Phase IV
Handles task management and delegation through natural language
"""

import os
from pathlib import Path
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from multiple possible locations
env_paths = [
    Path(__file__).parent.parent / ".env.local",  # src/backend/.env.local
    Path(__file__).parent.parent.parent.parent / ".env",  # project root .env
    ".env.local",  # current directory
]

for env_path in env_paths:
    if Path(env_path).exists():
        load_dotenv(env_path, override=True)
        break


class Orchestrator:
    """
    Main orchestrator for AI agent interactions.
    Delegates user queries to appropriate handlers.
    """
    
    def __init__(self):
        """Initialize the orchestrator with OpenAI client"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️  Warning: OPENAI_API_KEY not set. Agent features will be limited.")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)
    
    def delegate(self, query: str, context: str = "task") -> Dict[str, Any]:
        """
        Delegate a user query to the appropriate handler.
        
        Args:
            query: The user's natural language query
            context: Context hint (e.g., "task", "github", "weather")
        
        Returns:
            Dict containing the agent's response and any actions taken
        """
        if not self.client:
            return {
                "status": "error",
                "message": "OpenAI client not initialized. Please set OPENAI_API_KEY.",
                "query": query,
                "context": context
            }
        
        try:
            # Use OpenAI to interpret the query
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful task management assistant. "
                            "Interpret user queries and provide actionable responses. "
                            "For task-related queries, suggest task creation, updates, or completions. "
                            "Keep responses concise and actionable."
                        )
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            return {
                "status": "success",
                "query": query,
                "context": context,
                "response": ai_response,
                "model": "gpt-4o-mini",
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Agent error: {str(e)}",
                "query": query,
                "context": context
            }


# Global orchestrator instance
orchestrator = Orchestrator()
