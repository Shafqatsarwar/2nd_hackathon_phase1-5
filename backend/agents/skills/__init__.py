"""
AI Skills package for task analysis and enhancement
Contains specialized skills for the AI Agent.
"""

from .analysis import analyze_sentiment, suggest_tags
from .email_responder import generate_email_response, analyze_email_tone
from .meeting_minutes import generate_meeting_minutes, extract_action_items

__all__ = [
    "analyze_sentiment", 
    "suggest_tags",
    "generate_email_response",
    "analyze_email_tone",
    "generate_meeting_minutes",
    "extract_action_items"
]
