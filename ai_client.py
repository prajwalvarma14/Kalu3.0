import os
import json
from groq import Groq
from dotenv import load_dotenv
from .models import IssueAnalysis

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY or "your_groq_api_key" in GROQ_API_KEY:
    # Fallback or warning - for now, we'll assume it might be set later
    # But strictly speaking, we need it. 
    # For now, let's proceed, validation will happen at runtime.
    pass

client = Groq(api_key=GROQ_API_KEY)

def analyze_issue(issue_data: dict) -> IssueAnalysis:
    SYSTEM_PROMPT = """
    You are an AI-powered GitHub Issue Assistant.

    Return ONLY valid JSON in this exact format:
    {
      "summary": "A one-sentence summary of the user's problem or request.",
      "type": "bug | feature_request | documentation | question | other",
      "priority_value": 3,
      "priority_justification": "Brief justification for the score.",
      "suggested_labels": ["label1", "label2", "label3"],
      "potential_impact": "Impact on users if this issue is a bug."
    }
    """
    
    user_message = f"""
    Analyze the following issue and produce JSON matching the system schema.
    
    Issue Data:
    Title: {issue_data['title']}
    Body: {issue_data['body']}
    Comments: {issue_data['comments']}
    """
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_message,
            }
        ],
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"},
    )
    
    response_content = chat_completion.choices[0].message.content
    data = json.loads(response_content)
    
    # Merge fields to match the User's Required Schema
    # User wants: "priority_score": "X/5 - justification"
    p_val = data.get("priority_value", 1)
    p_just = data.get("priority_justification", "No justification provided.")
    
    # Construct the final field expected by models.py and the frontend
    data["priority_score"] = f"{p_val}/5 - {p_just}"
    
    # Remove temporary fields if strict validation is on (or just let pydantic ignore them)
    # We will pass 'data' to IssueAnalysis which only has 'priority_score' defined, 
    # so Pydantic will ignore extra fields by default or we can clean them.
    # To be safe, let's keep 'data' clean.
    final_data = {
        "summary": data["summary"],
        "type": data["type"],
        "priority_score": data["priority_score"],
        "suggested_labels": data["suggested_labels"],
        "potential_impact": data["potential_impact"]
    }
    
    return IssueAnalysis(**final_data)
