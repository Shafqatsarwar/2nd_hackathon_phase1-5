import os
import requests
import json
import time
import jwt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BACKEND_URL = "http://127.0.0.1:8000"
SECRET = os.getenv("BETTER_AUTH_SECRET", "my_super_secure_hackathon_secret_key_2025")
USER_ID = "admin"  # Using admin as a test user

def generate_test_token(user_id):
    payload = {
        "sub": user_id,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
        "iss": "todo-evolution"
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def test_chatbot_features():
    print(f"Starting AI Chatbot & MCP Tool Test - User: {USER_ID}")
    token = generate_test_token(USER_ID)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Check if backend is alive
    try:
        health = requests.get(f"{BACKEND_URL}/health")
        print(f"Backend Health: {health.status_code}")
    except:
        print("Backend is not running on http://127.0.0.1:8000")
        return

    test_queries = [
        "What is the weather in Lahore?",
        "Search for the latest gold rate in Pakistan",
        "List my tasks",
        "Create a task to 'Buy groceries for dinner' with high priority"
    ]

    for query in test_queries:
        print(f"\nQuery: '{query}'")
        try:
            # Note: The endpoint is a streaming response (text/event-stream)
            response = requests.post(
                f"{BACKEND_URL}/api/{USER_ID}/chat",
                json={"message": query},
                headers=headers,
                stream=True
            )
            
            print("Response: ", end="", flush=True)
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    print(chunk.decode('utf-8'), end="", flush=True)
            print()
        except Exception as e:
            print(f"Error during chatbot request: {e}")

if __name__ == "__main__":
    test_chatbot_features()
