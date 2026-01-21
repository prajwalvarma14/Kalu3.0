from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import AnalyzeRequest, IssueAnalysis
from .github_client import fetch_issue_data
from .ai_client import analyze_issue
import uvicorn

app = FastAPI(title="GitHub Issue Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze", response_model=IssueAnalysis)
async def analyze_issue_endpoint(request: AnalyzeRequest):
    try:
        # Extract owner and repo from URL
        # URL format: https://github.com/owner/repo
        path_segments = request.repo_url.path.strip("/").split("/")
        if len(path_segments) < 2:
            raise ValueError("Invalid GitHub Repository URL")
        
        owner = path_segments[-2]
        repo = path_segments[-1]
        
        if repo.endswith(".git"):
            repo = repo[:-4]
        
        # Fetch data
        issue_data = await fetch_issue_data(owner, repo, request.issue_number)
        
        # Analyze with AI
        analysis = analyze_issue(issue_data)
        
        return analysis
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
