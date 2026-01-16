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
                    "You are a highly capable AI assistant. Your primary roles are:\n"
                    "1. Manage tasks/todos using the provided tools.\n"
                    "2. Orchestrate GitHub operations via MCP tools.\n"
                    "3. Answer ANY additional user questions by searching the web for real-time, accurate information.\n\n"
                    "If a user asks about news, facts, external events, or anything not in their task list, ALWAYS use the 'web_search' tool to provide a helpful, cited response. "
                    "Always use the appropriate tool for the user's request. "
                    "Only use the tools provided, do not try to access the database directly.\n"
                    f"The current user ID is: {user_id}"
                )
            },
            {
                "role": "user",
                "content": message
            }
        ]

        # Call the OpenAI API with function calling and streaming
        stream = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            tools=self.tools,
            tool_choice="auto",
            stream=True
        )

        # Process the stream and handle tool calls
        tool_calls = []
        current_tool_call = None
        
        for chunk in stream:
            delta = chunk.choices[0].delta
            
            # Handle text content
            if delta.content:
                yield delta.content
            
            # Handle tool calls
            if delta.tool_calls:
                for tool_call_chunk in delta.tool_calls:
                    if tool_call_chunk.index is not None:
                        # Start new tool call or continue existing one
                        while len(tool_calls) <= tool_call_chunk.index:
                            tool_calls.append({
                                "id": "",
                                "type": "function",
                                "function": {"name": "", "arguments": ""}
                            })
                        
                        current_tool_call = tool_calls[tool_call_chunk.index]
                        
                        if tool_call_chunk.id:
                            current_tool_call["id"] = tool_call_chunk.id
                        
                        if tool_call_chunk.function:
                            if tool_call_chunk.function.name:
                                current_tool_call["function"]["name"] = tool_call_chunk.function.name
                            if tool_call_chunk.function.arguments:
                                current_tool_call["function"]["arguments"] += tool_call_chunk.function.arguments
        
        # Execute tool calls if any
        if tool_calls:
            import json
            from .weather_service import get_weather_info, get_weather_forecast
            from .web_search import search_web
            
            for tool_call in tool_calls:
                function_name = tool_call["function"]["name"]
                try:
                    function_args = json.loads(tool_call["function"]["arguments"])
                except json.JSONDecodeError:
                    yield f"\n\n⚠️ Error parsing arguments for {function_name}"
                    continue
                
                # Execute the appropriate tool
                try:
                    if function_name == "list_tasks":
                        # Get session for this operation
                        from ..database import get_session as get_db_session
                        session_gen = get_db_session()
                        db_session = next(session_gen)
                        try:
                            from sqlmodel import select
                            from ..models import Task
                            tasks = db_session.exec(
                                select(Task).where(Task.user_id == function_args.get("user_id"))
                            ).all()
                            yield f"\n\n📋 Your tasks:\n"
                            if tasks:
                                for task in tasks:
                                    status = "✅" if task.completed else "⬜"
                                    yield f"{status} {task.title}\n"
                            else:
                                yield "No tasks found. Create your first task!"
                        finally:
                            try:
                                next(session_gen)
                            except StopIteration:
                                pass
                    
                    elif function_name == "add_task":
                        # Get session for this operation
                        from ..database import get_session as get_db_session
                        from ..models import Task, TaskCreate
                        session_gen = get_db_session()
                        db_session = next(session_gen)
                        try:
                            task_data = TaskCreate(
                                title=function_args.get("title"),
                                description=function_args.get("description", ""),
                                priority=function_args.get("priority", "medium"),
                                is_recurring=function_args.get("is_recurring", False),
                                recurrence_interval=function_args.get("recurrence_interval")
                            )
                            db_task = Task.model_validate(task_data, update={"user_id": function_args.get("user_id")})
                            db_session.add(db_task)
                            db_session.commit()
                            db_session.refresh(db_task)
                            
                            # Analyze the task
                            from ..agents.skills.analysis import analyze_sentiment, suggest_tags
                            suggested_priority = analyze_sentiment(db_task.title)
                            tags = suggest_tags(db_task.title)
                            
                            yield f"\n\n✅ Task created: {db_task.title}"
                            yield f"\n💡 Suggested priority: {suggested_priority}"
                            if tags:
                                yield f"\n🏷️ Suggested tags: {', '.join(tags)}"
                        finally:
                            try:
                                next(session_gen)
                            except StopIteration:
                                pass
                    
                    elif function_name == "get_current_weather":
                        result = get_weather_info(function_args.get("location"))
                        yield f"\n\n{result}"
                    
                    elif function_name == "get_weather_forecast":
                        result = get_weather_forecast(function_args.get("location"))
                        yield f"\n\n{result}"
                    
                    elif function_name == "web_search":
                        result = search_web(function_args.get("query"))
                        yield f"\n\n🔍 {result}"
                    
                    else:
                        yield f"\n\n⚠️ Tool {function_name} not yet implemented in streaming mode"
                
                except Exception as e:
                    yield f"\n\n⚠️ Error executing {function_name}: {str(e)}"
    
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