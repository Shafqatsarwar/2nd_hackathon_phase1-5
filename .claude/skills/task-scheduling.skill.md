# Task Scheduling and Reminders Skill

## Purpose
This skill describes how to implement task scheduling and reminder functionality using event-driven architecture.

## When to Use
- When implementing due dates for tasks
- When setting up recurring tasks
- When building reminder systems
- When scheduling notifications
- When implementing time-based triggers

## Implementation Approaches
1. Dapr Jobs API for precise scheduling
2. Kafka streams for event-based scheduling
3. Background workers for processing scheduled tasks
4. Database-based queuing for delayed execution

## Dapr Jobs API Pattern
```python
import httpx
from datetime import datetime

async def schedule_reminder(task_id: int, remind_at: datetime, user_id: str):
    """Schedule reminder using Dapr Jobs API."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://localhost:3500/v1.0-alpha1/jobs/reminder-task-{task_id}",
            json={
                "dueTime": remind_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "data": {
                    "task_id": task_id,
                    "user_id": user_id,
                    "type": "reminder"
                }
            }
        )
        return response.status_code == 200

async def handle_job_trigger(request: Request):
    """Dapr calls this endpoint at the exact scheduled time."""
    job_data = await request.json()

    if job_data["data"]["type"] == "reminder":
        # Publish to notification service via Dapr PubSub
        await publish_event("reminders", "reminder.due", job_data["data"])

    return {"status": "SUCCESS"}
```

## Kafka-Based Scheduling Pattern
```python
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime
import threading
import time

class TaskScheduler:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
        self.consumer = KafkaConsumer('scheduled-tasks', bootstrap_servers=['localhost:9092'])

    def schedule_task(self, task_id, execution_time, payload):
        """Schedule a task for future execution."""
        event = {
            'task_id': task_id,
            'execute_at': execution_time.isoformat(),
            'payload': payload,
            'status': 'scheduled'
        }
        self.producer.send('scheduled-tasks', event)

    def start_scheduler(self):
        """Start the scheduler thread."""
        def process_scheduled_tasks():
            for message in self.consumer:
                task_event = json.loads(message.value)
                if datetime.fromisoformat(task_event['execute_at']) <= datetime.now():
                    # Process the scheduled task
                    self.execute_scheduled_task(task_event)

        scheduler_thread = threading.Thread(target=process_scheduled_tasks)
        scheduler_thread.daemon = True
        scheduler_thread.start()
```

## Recurring Tasks Implementation
- Define recurrence patterns (daily, weekly, monthly)
- Create task templates for recurring tasks
- Generate new tasks based on recurrence rules
- Track completion of recurring instances

## Database Schema for Scheduling
```sql
CREATE TABLE scheduled_tasks (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id),
    execute_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'scheduled',
    payload JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Error Handling
- Retry mechanisms for failed scheduled tasks
- Dead letter queues for permanently failed tasks
- Monitoring and alerting for scheduling failures
- Fallback mechanisms for critical scheduled operations