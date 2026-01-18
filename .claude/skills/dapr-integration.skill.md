# Dapr Integration Skill

## Purpose
This skill describes how to integrate Dapr for distributed application runtime capabilities.

## When to Use
- When implementing service-to-service communication
- When setting up state management
- When configuring pub/sub messaging
- When managing secrets securely
- When implementing job scheduling

## Dapr Building Blocks Used
1. Pub/Sub - for event-driven communication
2. State Management - for storing state reliably
3. Service Invocation - for service-to-service calls
4. Secrets Management - for secure credential access
5. Bindings - for connecting to external systems
6. Actors - for stateful services (optional)

## Implementation Steps
1. Install Dapr CLI and initialize in Kubernetes
2. Define Dapr components (pubsub, state store, secrets)
3. Update application to use Dapr sidecar
4. Replace direct service calls with Dapr service invocation
5. Replace direct state access with Dapr state management
6. Replace direct message queue access with Dapr pub/sub

## Dapr Annotations Example
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
spec:
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "todo-backend"
        dapr.io/app-port: "8000"
        dapr.io/components-path: "/dapr/components"
```

## Code Patterns
```python
import httpx

# Publishing to pubsub
async def publish_message(topic: str, data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://localhost:3500/v1.0/publish/pubsub/{topic}",
            json=data
        )
        return response.status_code == 200

# State management
async def save_state(key: str, value: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:3500/v1.0/state/statestore",
            json=[{
                "key": key,
                "value": value
            }]
        )
        return response.status_code == 200
```

## Configuration Files
- pubsub.yaml - Pub/sub component configuration
- statestore.yaml - State store component configuration
- secrets.yaml - Secrets store configuration