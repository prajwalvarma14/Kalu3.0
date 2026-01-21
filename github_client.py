import httpx
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

async def fetch_issue_data(owner: str, repo: str, issue_number: int):
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-Issue-Assistant"
    }
    if GITHUB_TOKEN and "your_github_token" not in GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    base_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    
    async with httpx.AsyncClient() as client:
        # Fetch Issue
        response = await client.get(base_url, headers=headers)
        if response.status_code == 404:
            raise ValueError("Issue not found or repository is private.")
        response.raise_for_status()
        issue_data = response.json()
        
        # Fetch Comments
        comments_url = issue_data["comments_url"]
        comments_response = await client.get(comments_url, headers=headers)
        comments_response.raise_for_status()
        comments_data = comments_response.json()
        
        comments_text = "\n".join([f"Comment by {c['user']['login']}: {c['body']}" for c in comments_data[:5]]) # Limit to first 5 comments

        return {
            "title": issue_data["title"],
            "body": issue_data["body"],
            "comments": comments_text
        }
