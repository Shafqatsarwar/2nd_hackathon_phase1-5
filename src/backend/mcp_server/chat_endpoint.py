from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from sqlmodel import Session
from ..database import get_session
from ..auth_utils import verify_jwt
from ..models import Conversation, Message
from .agent import TodoOpenAIAgent

# Import MCP server components conditionally to avoid breaking Phase II
try:
    from .mcp_server import mcp_server
    MCP_AVAILABLE = True
except ImportError as e:
    print(f"Warning: MCP server not available: {e}")
    MCP_AVAILABLE = False
    mcp_server = None


router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[Dict[str, Any]] = []


@router.post("/{user_id}/chat")
async def chat(
    user_id: str,
    request: ChatRequest = None,
    token_user_id: str = Depends(verify_jwt),
    session: Session = Depends(get_session)
):
    """
    Chat endpoint for the AI-powered todo chatbot.
    This is a stateless endpoint that stores conversation state in the database.
    All task operations are performed through MCP tools to ensure AI agents
    never access the database directly.
    """
    if user_id != token_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user's chat")

    # Get or create conversation
    conversation_id = request.conversation_id if request else None
    if not conversation_id:
        # Create new conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        conversation_id = conversation.id
    else:
        # Verify conversation belongs to user
        existing_conv = session.get(Conversation, conversation_id)
        if not existing_conv or existing_conv.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")

    # Store user message
    user_message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role="user",
        content=request.message if request else ""
    )
    session.add(user_message)
    session.commit()

    return StreamingResponse(process_natural_language_command(user_id, request.message if request else "", session), media_type="text/event-stream")


@router.get("/{user_id}/chat/history", response_model=List[Dict[str, Any]])
async def get_chat_history(
    user_id: str,
    token_user_id: str = Depends(verify_jwt),
    session: Session = Depends(get_session)
):
    """
    Fetch the most recent conversation history for a user.
    """
    if user_id != token_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    from sqlmodel import select
    conversation = session.exec(
        select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
    ).first()

    if not conversation:
        return []

    messages = session.exec(
        select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at.asc())
    ).all()

    return [
        {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "timestamp": msg.created_at.isoformat(),
            "conversation_id": msg.conversation_id
        }
        for msg in messages
    ]


async def process_natural_language_command(user_id: str, message: str, session: Session):
    """
    Process natural language command using OpenAI agent with MCP tools.
    This function integrates with the OpenAI API to process natural language
    and execute appropriate task operations through MCP tools.
    """
    # Initialize the OpenAI agent
    try:
        agent = TodoOpenAIAgent()
        async for chunk in agent.process_message(user_id, message, session):
            yield chunk
    except ValueError as e:
        # Environment variable not set
        error_msg = str(e)
        print(f"Configuration error: {error_msg}")
        yield f"Configuration error: {error_msg}"
    except Exception as e:
        # Fallback to a simple rule-based processor if OpenAI integration fails
        import traceback
        error_details = traceback.format_exc()
        print(f"OpenAI agent error: {e}")
        print(f"Full traceback:\n{error_details}")
        yield f"I encountered an issue processing your request: {str(e)}. Please check the server logs for details."