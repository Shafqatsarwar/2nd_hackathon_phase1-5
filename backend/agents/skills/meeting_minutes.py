"""
Meeting Minutes Generator Skill
Transforms raw meeting notes or transcripts into structured minutes.
"""

from typing import List, Dict, Optional
import datetime

def generate_meeting_minutes(
    notes: str,
    attendees: Optional[List[str]] = None,
    date: Optional[str] = None
) -> Dict[str, str]:
    """
    Parses notes to structure meeting minutes.
    
    Args:
        notes: Raw meeting notes or transcript
        attendees: List of participant names
        date: Date of the meeting (YYYY-MM-DD)
        
    Returns:
        Dictionary containing formatted sections: 'markdown', 'summary', 'actions'
    """
    
    if not date:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        
    attendees_str = ", ".join(attendees) if attendees else "All Team Members"
    
    # Process notes to find action items (simple keyword heuristic)
    lines = notes.split('\n')
    action_items = []
    key_points = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        lower_line = line.lower()
        if any(marker in lower_line for marker in ["todo", "action:", "task:", "assigned to"]):
            action_items.append(line)
        else:
            key_points.append(line)
            
    # Format Action Items
    actions_formatted = "\n".join([f"- [ ] {item}" for item in action_items]) if action_items else "- No specific action items extracted."
    
    # Format Summary (Key Points)
    summary_formatted = "\n".join([f"- {item}" for item in key_points]) if key_points else "No detailed notes provided."

    # Construct Markdown Report
    markdown_report = f"""# Meeting Minutes
**Date:** {date}
**Attendees:** {attendees_str}

## Summary
{summary_formatted}

## Action Items
{actions_formatted}
"""

    return {
        "markdown": markdown_report,
        "summary": summary_formatted,
        "actions": actions_formatted,
        "raw_date": date
    }

def extract_action_items(text: str) -> List[str]:
    """
    Extracts just the action items from a text block.
    """
    minutes = generate_meeting_minutes(text)
    return minutes["actions"].split('\n')
