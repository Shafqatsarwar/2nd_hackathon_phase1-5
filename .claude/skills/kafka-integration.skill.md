# Kafka Integration Skill

## Purpose
This skill describes how to integrate Kafka for event-driven architecture in the Todo application.

## When to Use
- When implementing recurring tasks
- When setting up reminder systems
- When building event-driven processing
- When implementing audit logging
- When enabling real-time synchronization

## Implementation Steps
1. Set up Kafka producer to publish task events
2. Set up Kafka consumer to process task events
3. Define event schemas for different task operations
4. Integrate with existing task management API
5. Ensure proper error handling and retries

## Event Types
- task-created
- task-updated
- task-completed
- task-deleted
- task-reminder

## Code Patterns
```python
from kafka import KafkaProducer
import json

def publish_task_event(event_type, task_data):
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    event = {
        'event_type': event_type,
        'task_data': task_data,
        'timestamp': datetime.utcnow().isoformat()
    }
    producer.send('task-events', event)
```

## Integration Points
- Task creation endpoints
- Task update endpoints
- Reminder scheduling system
- Audit logging system