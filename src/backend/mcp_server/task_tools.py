from typing import List, Dict, Any
from sqlmodel import select
from ..models import Task, TaskCreate
from ..agents.skills.analysis import analyze_sentiment, suggest_tags


class MCPTaskTools:
    """
    MCP Tools for task operations that can be called by AI agents
    """

    def __init__(self, session_getter):
        self.get_session = session_getter

    def add_task(self, user_id: str, title: str, description: str = None, priority: str = "medium", is_recurring: bool = False, recurrence_interval: str = None) -> Dict[str, Any]:
        """
        MCP Tool: Create a new task
        """
        with self.get_session() as session:
            task_data = TaskCreate(
                title=title,
                description=description or "",
                priority=priority,
                is_recurring=is_recurring,
                recurrence_interval=recurrence_interval
            )
            db_task = Task.model_validate(task_data, update={"user_id": user_id})
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            # Integrate Agent Skills: Analyze the task for +200 Bonus points
            priority = analyze_sentiment(db_task.title)
            tags = suggest_tags(db_task.title)

            return {
                "task_id": db_task.id,
                "status": "created",
                "title": db_task.title,
                "description": db_task.description,
                "priority": db_task.priority,
                "is_recurring": db_task.is_recurring,
                "recurrence_interval": db_task.recurrence_interval,
                "completed": db_task.completed,
                "analysis": {
                    "suggested_priority": priority,
                    "suggested_tags": tags
                }
            }

    def list_tasks(self, user_id: str, status: str = "all") -> List[Dict[str, Any]]:
        """
        MCP Tool: Retrieve tasks from the list
        """
        with self.get_session() as session:
            query = select(Task).where(Task.user_id == user_id)

            if status == "pending":
                query = query.where(Task.completed.is_(False))
            elif status == "completed":
                query = query.where(Task.completed.is_(True))

            tasks = session.exec(query).all()

            return [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "is_recurring": task.is_recurring,
                    "recurrence_interval": task.recurrence_interval
                }
                for task in tasks
            ]

    def complete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """
        MCP Tool: Mark a task as complete
        """
        with self.get_session() as session:
            db_task = session.exec(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            ).first()

            if not db_task:
                return {
                    "error": f"Task {task_id} not found for user {user_id}",
                    "status": "error"
                }

            db_task.completed = True
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            return {
                "task_id": db_task.id,
                "status": "completed",
                "title": db_task.title
            }

    def delete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """
        MCP Tool: Remove a task from the list
        """
        with self.get_session() as session:
            db_task = session.exec(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            ).first()

            if not db_task:
                return {
                    "error": f"Task {task_id} not found for user {user_id}",
                    "status": "error"
                }

            session.delete(db_task)
            session.commit()

            return {
                "task_id": task_id,
                "status": "deleted",
                "title": db_task.title
            }

    def update_task(self, user_id: str, task_id: int, title: str = None, description: str = None, priority: str = None, is_recurring: bool = None, recurrence_interval: str = None) -> Dict[str, Any]:
        """
        MCP Tool: Modify task title or description
        """
        with self.get_session() as session:
            db_task = session.exec(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            ).first()

            if not db_task:
                return {
                    "error": f"Task {task_id} not found for user {user_id}",
                    "status": "error"
                }

            if title is not None:
                db_task.title = title
            if description is not None:
                db_task.description = description
            if priority is not None:
                db_task.priority = priority
            if is_recurring is not None:
                db_task.is_recurring = is_recurring
            if recurrence_interval is not None:
                db_task.recurrence_interval = recurrence_interval

            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            return {
                "task_id": db_task.id,
                "status": "updated",
                "title": db_task.title
            }