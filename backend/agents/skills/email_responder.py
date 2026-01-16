"""
Email Responder Skill
Generates professional email responses based on input content and tone.
"""

from typing import Optional

def generate_email_response(
    email_content: str,
    sender_name: str = "Sender",
    user_name: str = "User",
    tone: str = "professional",
    context: Optional[str] = None
) -> str:
    """
    Generates a structured email response template.
    
    Args:
        email_content: The content of the email to reply to
        sender_name: The name of the person who sent the email
        user_name: The name of the user sending the reply
        tone: The desired tone (professional, casual, friendly, formal)
        context: Additional context for the reply (optional)
        
    Returns:
        A formatted email response string
    """
    
    # Determine greeting and sign-off based on tone
    if tone == "casual":
        greeting = f"Hi {sender_name},"
        sign_off = "Best,"
    elif tone == "friendly":
        greeting = f"Hello {sender_name},"
        sign_off = "Cheers,"
    elif tone == "formal":
        greeting = f"Dear {sender_name},"
        sign_off = "Sincerely,"
    else:  # professional
        greeting = f"Dear {sender_name},"
        sign_off = "Best regards,"

    # Construct the body template
    # In a real AI implementation, this would call an LLM. 
    # Here we provide a high-quality template for the Agent to fill.
    
    topic_reference = f"regarding your email about '{email_content[:50]}...'" if email_content else "regarding your recent email"
    
    body = f"""
{greeting}

Thank you for contacting me {topic_reference}.

I have received your message and wanted to get back to you {context if context else 'promptly'}.

[AI: INSERT GENERATED RESPONSE BODY HERE BASED ON CONTENT AND CONTEXT]

Please let me know if you need any further information.

{sign_off}
{user_name}
"""
    return body.strip()

def analyze_email_tone(email_content: str) -> str:
    """
    Simple heuristic to guess the tone of an incoming email.
    """
    content_lower = email_content.lower()
    
    if any(word in content_lower for word in ["hey", "hi", "what's up", "cool"]):
        return "casual"
    elif any(word in content_lower for word in ["fail", "error", "urgent", "problem"]):
        return "professional"  # Keep professional in crises
    elif any(word in content_lower for word in ["dear", "sincerely", "regards"]):
        return "formal"
    
    return "professional"
