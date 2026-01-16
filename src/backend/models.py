from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str = Field(index=True, unique=True)
    full_name: Optional[str] = None

    tasks: List["Task"] = Relationship(back_populates="user")
    conversations: List["Conversation"] = Relationship(back_populates="user")
    messages: List["Message"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False)
    priority: str = Field(default="medium")
    is_recurring: bool = Field(default=False)
    recurrence_interval: Optional[str] = None

    user_id: str = Field(foreign_key="user.id", index=True)
    user: Optional[User] = Relationship(back_populates="tasks")

class Conversation(SQLModel, table=True):
    """
    Database model for chat conversations
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    """
    Database model for chat messages
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    role: str  # 'user' or 'assistant'
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="messages")
    conversation: Optional[Conversation] = Relationship(back_populates="messages")

class TaskCreate(SQLModel):
    title: str = Field(..., schema_extra={"examples": ["Complete Task"]})
    description: Optional[str] = Field(None, schema_extra={"examples": ["Task description"]})
    priority: Optional[str] = Field("medium", schema_extra={"examples": ["high"]})
    is_recurring: bool = Field(False, schema_extra={"examples": [True]})
    recurrence_interval: Optional[str] = Field(None, schema_extra={"examples": ["daily"]})

class TaskUpdate(SQLModel):
    title: Optional[str] = Field(None, schema_extra={"examples": ["Updated Task Title"]})
    description: Optional[str] = Field(None, schema_extra={"examples": ["Updated description"]})
    completed: Optional[bool] = Field(None, schema_extra={"examples": [True]})
    priority: Optional[str] = Field(None, schema_extra={"examples": ["high"]})
    is_recurring: Optional[bool] = Field(None, schema_extra={"examples": [True]})
    recurrence_interval: Optional[str] = Field(None, schema_extra={"examples": ["daily"]})
