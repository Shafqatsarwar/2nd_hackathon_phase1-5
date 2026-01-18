import os
from openai import OpenAI
from .task_tools import MCPTaskTools
from .github_tools import GitHubMCPTools, GITHUB_TOOLS
from ..database import get_session
from sqlmodel import Session



class TodoOpenAIAgent:
    """
    OpenAI Agent that uses MCP tools to interact with the todo system
    """

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.demo_mode = False
        
        if not api_key:
            print("⚠️  Warning: OPENAI_API_KEY not set. Running in DEMO MODE.")
            self.demo_mode = True
            self.client = None
        else:
            try:
                self.client = OpenAI(api_key=api_key)
                # Test the API key with a simple call
                print("✅ OpenAI client initialized successfully")
            except Exception as e:
                print(f"⚠️  Warning: OpenAI API key invalid. Running in DEMO MODE. Error: {e}")
                self.demo_mode = True
                self.client = None

        # Initialize tools
        self.github_tools = GitHubMCPTools()
        self.task_tools = MCPTaskTools(get_session)

        # Define the tools that the agent can use
        self.tools = [
            # Task management tools
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"},
                            "title": {"type": "string", "description": "Task title"},
                            "description": {"type": "string", "description": "Task description (optional)"},
                            "priority": {"type": "string", "enum": ["low", "medium", "high"], "default": "medium", "description": "Task priority level"},
                            "is_recurring": {"type": "boolean", "default": False, "description": "Whether the task is recurring"},
                            "recurrence_interval": {"type": "string", "description": "How often the task recurs (e.g., daily, weekly, monthly)"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Retrieve tasks from the list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"},
                            "status": {"type": "string", "enum": ["all", "pending", "completed"], "default": "all"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as complete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"},
                            "task_id": {"type": "integer", "description": "The task ID to complete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Remove a task from the list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"},
                            "task_id": {"type": "integer", "description": "The task ID to delete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Modify task title or description",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"},
                            "task_id": {"type": "integer", "description": "The task ID to update"},
                            "title": {"type": "string", "description": "New title (optional)"},
                            "description": {"type": "string", "description": "New description (optional)"},
                            "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "New priority level (optional)"},
                            "is_recurring": {"type": "boolean", "description": "Whether the task is recurring (optional)"},
                            "recurrence_interval": {"type": "string", "description": "How often the task recurs (optional)"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]

        # Add GitHub tools to the agent
        self.tools.extend(GITHUB_TOOLS)

        # Add web search tool to the agent
        self.tools.append({
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Search the web for current information, news, market rates, and other public information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query for information"}
                    },
                    "required": ["query"]
                }
            }
        })

        # Add weather tools to the agent
        self.tools.append({
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get current weather information for a specific location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "Location to get weather for (e.g., 'Lahore, Pakistan', 'Karachi', 'Islamabad')"}
                    },
                    "required": ["location"]
                }
            }
        })

        self.tools.append({
            "type": "function",
            "function": {
                "name": "get_weather_forecast",
                "description": "Get weather forecast for a specific location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "Location to get forecast for (e.g., 'Lahore, Pakistan', 'Karachi', 'Islamabad')"}
                    },
                    "required": ["location"]
                }
            }
        })

        self.tools.append({
            "type": "function",
            "function": {
                "name": "get_smart_insight",
                "description": "Get a motivational quote and an analysis of your current workload",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        })

    async def process_message(self, user_id: str, message: str, session: Session):
        """
        Process a user message using OpenAI agent with MCP tools and stream the response.
        Falls back to demo mode if OpenAI API is not available.
        """
        # Demo mode - provide helpful responses without OpenAI
        if self.demo_mode:
            demo_response = self._get_demo_response(message, user_id)
            for char in demo_response:
                yield char
            return
        
        # Prepare the messages for the OpenAI API
        messages = [
            {
                "role": "system",
                "content": (
                    "You are 'Evolution AI', a premium task assistant. Your personality is helpful, professional, and proactive.\n\n"
                    "CORE CAPABILITIES:\n"
                    "1. Task Management: Use tools to add, list, complete, or delete tasks. Be smart about priorities.\n"
                    "2. GitHub Operations: Handle issues and PRs for the user.\n"
                    "3. Real-time Search: Use 'web_search' for news, facts, market rates, and current events.\n"
                    "4. Weather: Use weather tools to provide localized updates.\n\n"
                    "STRICT RULES:\n"
                    "- ALWAYS use the 'web_search' tool for external facts (news, sports, gold rates, etc.).\n"
                    "- If the weather is 'Rainy' or 'Snowy' and the user creates a task that sounds like an outdoor activity (e.g., 'Jogging', 'Car wash'), gently warn them.\n"
                    "- If the user's task list is crowded (>5 pending tasks), suggest a priority focus.\n"
                    "- When using tools, summarize the result naturally. DON'T just dump raw JSON or raw tool output.\n"
                    f"- Current User Context: {user_id}"
                )
            },
            {
                "role": "user",
                "content": message
            }
        ]

        # Max number of tool-calling loops to prevent infinite loops
        max_iterations = 5
        
        for iteration in range(max_iterations):
            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4o-mini", # Upgraded from gpt-3.5-turbo
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )
            
            assistant_message = response.choices[0].message
            messages.append(assistant_message)
            
            # If no tool calls, we're done - yield the final content
            if not assistant_message.tool_calls:
                if assistant_message.content:
                    yield assistant_message.content
                break
                
            # Execute tool calls
            import json
            from .weather_service import get_weather_info, get_weather_forecast
            from .web_search import search_web
            
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                try:
                    function_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": "Error: Invalid JSON arguments"
                    })
                    continue
                
                print(f"DEBUG: Executing tool '{function_name}' with args {function_args}")
                yield f"... Thinking... (using {function_name})\n"
                
                tool_result = ""
                try:
                    if function_name == "list_tasks":
                        from ..database import get_session as get_db_session
                        from sqlmodel import select
                        from ..models import Task
                        session_gen = get_db_session()
                        db_session = next(session_gen)
                        tasks = db_session.exec(select(Task).where(Task.user_id == user_id)).all()
                        tool_result = "\n".join([f"- [{ 'X' if t.completed else ' ' }] ID {t.id}: {t.title} ({t.priority})" for t in tasks]) or "No tasks found."
                    
                    elif function_name == "add_task":
                        from ..database import get_session as get_db_session
                        from ..models import Task, TaskCreate
                        session_gen = get_db_session()
                        db_session = next(session_gen)
                        task_data = TaskCreate(
                            title=function_args.get("title"),
                            description=function_args.get("description", ""),
                            priority=function_args.get("priority", "medium")
                        )
                        db_task = Task.model_validate(task_data, update={"user_id": user_id})
                        db_session.add(db_task)
                        db_session.commit()
                        db_session.refresh(db_task)
                        tool_result = f"Successfully created task ID {db_task.id}: {db_task.title}"
                    
                    elif function_name == "get_smart_insight":
                        from ..database import get_session as get_db_session
                        from sqlmodel import select
                        from ..models import Task
                        from ..agents.skills.advisor import get_smart_insight as advisor_insight
                        session_gen = get_db_session()
                        db_session = next(session_gen)
                        tasks = db_session.exec(select(Task).where(Task.user_id == user_id)).all()
                        task_dicts = [{"title": t.title, "priority": t.priority, "completed": t.completed} for t in tasks]
                        tool_result = advisor_insight(user_id, task_dicts)
                    
                    elif function_name == "get_current_weather":
                        tool_result = get_weather_info(function_args.get("location"))
                    
                    elif function_name == "web_search":
                        tool_result = search_web(function_args.get("query"))
                    
                    elif function_name in ["create_github_issue", "create_pull_request", "list_repositories"]:
                        # Re-use the existing github tools logic
                        tool_result = self.github_tools.call_function(function_name, function_args)
                        
                    else:
                        tool_result = f"Error: Tool '{function_name}' is not yet fully implemented in the orchestrator."
                
                except Exception as e:
                    tool_result = f"Error executing tool: {str(e)}"
                
                # Add tool result to conversation history
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": tool_result
                })
    
    def _get_demo_response(self, message: str, user_id: str) -> str:
        """
        Provide demo responses when OpenAI API is not available.
        """
        message_lower = message.lower()
        
        # Greetings
        if any(word in message_lower for word in ['hi', 'hello', 'hey', 'greetings']):
            return "Hello! 👋 I'm running in demo mode (OpenAI API not available). I can still help you manage tasks! Try asking me to create a task or list your tasks."
        
        # Task-related queries
        if any(word in message_lower for word in ['task', 'todo', 'create', 'add', 'list', 'show']):
            return "I can help you manage tasks! In demo mode, I can explain how to use the task features. To actually create tasks, please use the task management UI or get a valid OpenAI API key. Would you like me to explain the available features?"
        
        # Weather queries
        if 'weather' in message_lower:
            if 'lahore' in message_lower:
                return "🌤️ Demo Mode Response: Lahore typically has hot summers and mild winters. For real-time weather data, please configure a valid OpenAI API key. The actual weather feature uses live data from weather APIs."
            return "🌤️ Demo Mode Response: I can provide weather information when connected to OpenAI. Please configure a valid API key to get real-time weather data."
        
        # General queries
        return f"Demo Mode: I received your message '{message}'. To get AI-powered responses, please configure a valid OpenAI API key in your environment variables. For now, I can help explain the task management features!"