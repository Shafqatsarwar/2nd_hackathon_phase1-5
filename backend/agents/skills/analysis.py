"""
AI Skills for task analysis
Provides sentiment analysis and tag suggestions for tasks
"""

from typing import List


def analyze_sentiment(text: str) -> str:
    """
    Analyze the sentiment/urgency of a task title to suggest priority.
    
    Args:
        text: The task title or description
    
    Returns:
        Suggested priority level: "high", "medium", or "low"
    """
    if not text:
        return "medium"
    
    text_lower = text.lower()
    
    # High priority keywords
    high_priority_keywords = [
        "urgent", "asap", "critical", "emergency", "immediately", 
        "deadline", "important", "bug", "fix", "broken", "error",
        "crash", "down", "failing", "security"
    ]
    
    # Low priority keywords
    low_priority_keywords = [
        "maybe", "someday", "eventually", "consider", "nice to have",
        "optional", "when possible", "low priority", "minor"
    ]
    
    # Check for high priority
    for keyword in high_priority_keywords:
        if keyword in text_lower:
            return "high"
    
    # Check for low priority
    for keyword in low_priority_keywords:
        if keyword in text_lower:
            return "low"
    
    # Default to medium
    return "medium"


def suggest_tags(text: str) -> List[str]:
    """
    Suggest relevant tags based on task content.
    
    Args:
        text: The task title or description
    
    Returns:
        List of suggested tags
    """
    if not text:
        return []
    
    text_lower = text.lower()
    suggested_tags = []
    
    # Category-based tag suggestions
    tag_mappings = {
        "work": ["work", "job", "office", "meeting", "project", "deadline"],
        "personal": ["personal", "home", "family", "self"],
        "shopping": ["buy", "purchase", "shop", "order", "get"],
        "health": ["health", "exercise", "gym", "doctor", "appointment"],
        "finance": ["pay", "bill", "invoice", "money", "budget", "finance"],
        "learning": ["learn", "study", "read", "course", "tutorial", "practice"],
        "development": ["code", "develop", "build", "implement", "debug", "test", "deploy"],
        "design": ["design", "ui", "ux", "mockup", "wireframe", "prototype"],
        "communication": ["email", "call", "message", "reply", "contact", "reach out"],
        "planning": ["plan", "organize", "schedule", "prepare", "arrange"],
        "urgent": ["urgent", "asap", "critical", "emergency", "immediately"],
        "bug": ["bug", "fix", "error", "issue", "problem", "broken"],
        "feature": ["feature", "add", "new", "implement", "create"],
        "documentation": ["document", "write", "readme", "guide", "docs"],
        "review": ["review", "check", "verify", "validate", "approve"]
    }
    
    # Check each category
    for tag, keywords in tag_mappings.items():
        for keyword in keywords:
            if keyword in text_lower:
                if tag not in suggested_tags:
                    suggested_tags.append(tag)
                break  # Only add the tag once per category
    
    # Limit to top 5 most relevant tags
    return suggested_tags[:5]
