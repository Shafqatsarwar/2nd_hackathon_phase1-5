import sys
import traceback
from pathlib import Path

# Add project root to sys.path to support both Vercel and local runs
root = Path(__file__).parent.parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))

from fastapi import FastAPI, Depends, HTTPException, status, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from sqlmodel import Session, select
from typing import List, Dict, Any
from pydantic import BaseModel
from src.backend.database import create_db_and_tables, get_session, engine
from src.backend.models import Task, TaskCreate, TaskUpdate, User
from src.backend.auth_utils import verify_jwt

app = FastAPI(title="The Evolution of Todo - Phase IV")


class RootResponse(BaseModel):
    message: str
    status: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Welcome to Phase IV Backend",
                "status": "Ready"
            }
        }
    }


def custom_openapi() -> Dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description=(
            "🚀 **The Evolution of Todo - Phase IV Backend**\n\n"
            "Manage tasks via REST API or AI Chat. Authenticate using specific access tokens.\n\n"
            "### 🔑 Authentication Instructions\n"
            "1. Click the **Authorize** button below.\n"
            "2. For **Admin Access**:\n"
            "   - Key: `admin` (Use this in `user_id` fields)\n"
            "   - Value: `admin_token` (Enter this in the Bearer token field)\n"
            "3. For **Guest Access**:\n"
            "   - Key: `guest_user` (Use this in `user_id` fields)\n"
            "   - Value: `guest_token` (Enter this in the Bearer token field)\n"
            "4. After clicking **Authorize**, the lock icon will close, indicating you are **Authorized**."
        ),
        routes=app.routes,
    )

    security_schemes = schema.setdefault("components", {}).setdefault("securitySchemes", {})
    security_schemes["bearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "Enter `admin_token` for Admin or `guest_token` for Guest access."
    }
    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    # Seed Admin User
    with Session(engine) as session:
        admin_email = "khansarwar1@hotmail.com"
        admin_id = "admin" # Fixed ID for consistency
        existing = session.exec(select(User).where(User.email == admin_email)).first()
        if not existing:
            admin_user = User(id=admin_id, email=admin_email, full_name="Admin")
            session.add(admin_user)
            session.commit()
            print(f"✅ Admin user seeded: {admin_email}")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In development, allow all - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=RootResponse)
def read_root():
    return RootResponse(message="Welcome to Phase IV Backend", status="Ready")

# --- TASK CRUD ENDPOINTS ---

@app.get(
    "/api/{user_id}/tasks",
    response_model=List[Task],
    responses={
        200: {
            "description": "List of tasks owned by the user",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "title": "Sync with Phase III",
                            "description": "Ensure the chat agent picks up new MCP tools.",
                            "completed": False,
                            "user_id": "admin"
                        },
                        {
                            "id": 2,
                            "title": "Finalize Better Auth",
                            "description": "Deploy backend + frontend secrets to Vercel.",
                            "completed": True,
                            "user_id": "admin"
                        }
                    ]
                }
            }
        }
    }
)
def list_tasks(
    user_id: str = Path(..., examples=["admin"], description="Enter 'admin' or 'guest_user'"),
    token_user_id: str = Depends(verify_jwt),
    session: Session = Depends(get_session)
):
    if user_id != token_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user's tasks")

    try:
        tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        return tasks
    except Exception:
        print(f"list_tasks failed for user_id={user_id} token_user_id={token_user_id}")
        traceback.print_exc()
        raise

@app.post("/api/{user_id}/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: str = Path(..., examples=["admin"], description="Enter 'admin' or 'guest_user'"),
    task: TaskCreate = None,
    token_user_id: str = Depends(verify_jwt),
    session: Session = Depends(get_session)
):
    if user_id != token_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to create tasks for this user")

    try:
        db_user = session.get(User, user_id)
        if not db_user:
            db_user = User(id=user_id, email=f"{user_id}@example.com")
            session.add(db_user)

        db_task = Task.model_validate(task, update={"user_id": user_id})
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
    except Exception as e:
        session.rollback()
        # Detailed error for debugging Phase III
        print(f"ERROR creating task: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Backend Error: {type(e).__name__}: {str(e)}"
        )

@app.get("/api/{user_id}/tasks/{id}", response_model=Task)
def get_task(
    user_id: str = Path(..., examples=["admin"], description="Enter 'admin' or 'guest_user'"),
    id: int = Path(..., examples=[1], description="The ID of the task to retrieve"),
    token_user_id: str = Depends(verify_jwt),
    session: Session = Depends(get_session)
):
    if user_id != token_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    task = session.exec(select(Task).where(Task.id == id, Task.user_id == user_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/api/{user_id}/tasks/{id}", response_model=Task)
def update_task_all(
    user_id: str = Path(..., examples=["admin"], description="Enter 'admin' or 'guest_user'"),
    id: int = Path(..., examples=[1], description="The ID of the task to update"),
    task: TaskUpdate = None,
    token_user_id: str = Depends(verify_jwt),
    session: Session = Depends(get_session)
):
    if user_id != token_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db_task = session.exec(select(Task).where(Task.id == id, Task.user_id == user_id)).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@app.patch("/api/{user_id}/tasks/{id}/complete", response_model=Task)
def toggle_task(
    user_id: str = Path(..., examples=["admin"], description="Enter 'admin' or 'guest_user'"),
    id: int = Path(..., examples=[1], description="The ID of the task to toggle"),
    token_user_id: str = Depends(verify_jwt),
    session: Session = Depends(get_session)
):
    if user_id != token_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db_task = session.exec(select(Task).where(Task.id == id, Task.user_id == user_id)).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.completed = not db_task.completed
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@app.delete("/api/{user_id}/tasks/{id}")
def delete_task(
    user_id: str = Path(..., examples=["admin"], description="Enter 'admin' or 'guest_user'"),
    id: int = Path(..., examples=[1], description="The ID of the task to delete"),
    token_user_id: str = Depends(verify_jwt),
    session: Session = Depends(get_session)
):
    if user_id != token_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db_task = session.exec(select(Task).where(Task.id == id, Task.user_id == user_id)).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(db_task)
    session.commit()
    return {"ok": True}

@app.get("/health")
def health_check(session: Session = Depends(get_session)):
    try:
        # Check DB connection
        session.exec(select(1)).first()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}

@app.get("/health/openai")
def openai_health_check():
    """
    Diagnostic endpoint to check if OpenAI client can be initialized.
    This helps debug Vercel deployment issues.
    """
    import os
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {
                "status": "error",
                "message": "OPENAI_API_KEY environment variable is not set",
                "env_vars_present": list(os.environ.keys())[:10]  # Show first 10 env vars for debugging
            }

        # Try to initialize OpenAI client
        from openai import OpenAI
        OpenAI(api_key=api_key)

        return {
            "status": "healthy",
            "message": "OpenAI client initialized successfully",
            "api_key_prefix": api_key[:10] + "..." if len(api_key) > 10 else "too_short"
        }
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }

# --- AGENT ENDPOINTS (PHASE III) ---
from src.backend.agents.orchestrator import orchestrator


class AgentRequest(BaseModel):
    query: str = "Fix the login bug asap"
    context: str = "task"

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query": "Buy milk and eggs",
                    "context": "task"
                }
            ]
        }
    }

@app.post("/api/agent/consult")
def consult_agent(request: AgentRequest):
    """
    Direct interface to the Backend Agent System.
    """
    return orchestrator.delegate(request.query, request.context)

# --- MCP CHAT ENDPOINT (PHASE III) ---
from src.backend.mcp_server.chat_endpoint import router as chat_router
app.include_router(chat_router)
print("✅ Chat router successfully included")
