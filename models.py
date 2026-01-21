from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional

class AnalyzeRequest(BaseModel):
    repo_url: HttpUrl
    issue_number: int

class IssueAnalysis(BaseModel):
    summary: str = Field(..., description="A one-sentence summary of the user's problem or request.")
    type: str = Field(..., description="Classify the issue as one of the following: bug, feature_request, documentation, question, or other.")
    priority_score: str = Field(..., description="X/5 - brief justification")
    suggested_labels: List[str] = Field(..., description="An array of relevant GitHub labels.")
    potential_impact: str = Field(..., description="A brief sentence on the potential impact on users if the issue is a bug.")
