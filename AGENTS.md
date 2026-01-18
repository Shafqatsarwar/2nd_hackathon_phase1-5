# AI Agents & Intelligence Documentation

This document outlines the AI agents, skills, and intelligent features integrated into the **Evolution of Todo** application.

## 🤖 Core Agents

### 1. Evolution AI (Main Chatbot Agent)
**Role:** The primary interface for user interaction in the application. It acts as a proactive, professional task assistant.
- **Location:** `src/backend/mcp_server/agent.py` (`TodoOpenAIAgent`)
- **Model:** `gpt-4o-mini`
- **Personality:** Helpful, professional, proactive.
- **Capabilities:**
  - **Task Management**: Create, list, update, complete, and delete tasks.
  - **GitHub Operations**: Create issues, pull requests, list repositories.
  - **Real-time Knowledge**: Web search for news, market rates, and facts.
  - **Weather Updates**: Real-time weather information and forecasts.
  - **Smart Insights**: Motivational quotes and workload analysis.

**Tools & Skills:**
| Tool Name | Description |
|-----------|-------------|
| `add_task` | Creates a new task with priority and optional recurrence. |
| `list_tasks` | Retrieves tasks filtered by status. |
| `complete_task` | Marks a task as completed. |
| `delete_task` | Removes a task. |
| `update_task` | Modifies task details (title, description, priority). |
| `web_search` | Searches the web using DuckDuckGo (via `duckduckgo-search`). |
| `get_current_weather` | Fetches current weather for a location. |
| `get_weather_forecast` | Fetches weather forecast. |
| `get_smart_insight` | Generates motivational advice based on current workload. |
| `create_github_issue` | Creates an issue in a GitHub repository. |
| `create_pull_request` | Creates a PR in a GitHub repository. |

### 2. Orchestrator
**Role:** Handles natural language task delegation and intent recognition.
- **Location:** `src/backend/agents/orchestrator.py`
- **Model:** `gpt-4o-mini`
- **Function:** Analyzes user queries to determine the appropriate context (task, github, weather, etc.) and delegates to the correct handler.

---

## 🧠 AI Skills
Specialized modules that provide specific intelligence capabilities. Located in `src/backend/agents/skills/`.

### 1. Advisor (`advisor.py`)
- **Purpose:** Provides "Smart Insights" to the user.
- **Features:**
  - **Workload Analysis:** Checks task density and high-priority items to give tailored advice (e.g., "Your plate is full, focus on high priority tasks").
  - **Motivation:** Serves tailored motivational quotes.

### 2. Analysis (`analysis.py`)
- **Purpose:** Text analysis utilities.
- **Features:**
  - **Sentiment Analysis:** (Planned) Analyze user sentiment.
  - **Tag Suggestion:** (Planned) Auto-tag tasks based on content.

### 3. Email Responder (`email_responder.py`)
- **Purpose:** Assist with email drafting.
- **Features:**
  - **Tone Analysis:** Detect email tone.
  - **Response Generation:** Draft email responses.

### 4. Meeting Minutes (`meeting_minutes.py`)
- **Purpose:** Process meeting content.
- **Features:**
  - **Minutes Generation:** Summarize meeting notes.
  - **Action Item Extraction:** Extract tasks from meeting text.

---

## 🛠️ Configuration

These agents require the following environment variables to function correctly:

| Variable | Description | Required? |
|----------|-------------|-----------|
| `OPENAI_API_KEY` | Key for accessing OpenAI models (`gpt-4o-mini`). | **Yes** |
| `GITHUB_TOKEN` | Personal Access Token for GitHub operations. | Optional (for GitHub tools) |
| `BETTER_AUTH_SECRET` | Secret for authentication security. | **Yes** |

## 🔗 Architecture

The AI system uses the **Model Context Protocol (MCP)** pattern where the agent acts as a client that can call various tools (functions) exposed by the system.
- **Frontend** acts as the user interface, sending chat messages to the backend.
- **Backend (FastAPI)** receives messages at `/api/{user_id}/chat`.
- **TodoOpenAIAgent** processes the message, calls necessary tools (SQLModel, External APIs), and streams the text response back to the client.
