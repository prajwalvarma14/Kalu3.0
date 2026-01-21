# AI-Powered GitHub Issue Assistant

A web application that helps developers categorize and prioritize GitHub issues using AI.

## Setup

1.  **Prerequisites**: Ensure you have Python installed.
2.  **Navigate to the project directory**:
    ```bash
    cd "c:/Users/PRAJWAL VARMA/OneDrive/Desktop/Kalu.3.0"
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment**:
    - Open `.env` file.
    - Add your `GROQ_API_KEY`.
    - (Optional) Add `GITHUB_TOKEN` for higher API rate limits.

## Running the Application

You need to run the Backend and Frontend in separate terminals.

### 1. Start Backend (API)
Open a terminal and run:
```bash
uvicorn backend.main:app --reload
```
The API will start at `http://127.0.0.1:8000`.

### 2. Start Frontend (UI)
Open **another** terminal and run:
```bash
streamlit run frontend/app.py
```
The browser will open automatically at `http://localhost:8501`.

## Usage
1.  Paste a public GitHub Repository URL (e.g., `https://github.com/facebook/react`).
2.  Enter an Issue Number (e.g., `123`).
3.  Click **Analyze Issue**.
4.  View the AI-generated Summary, Priority, and Labels.
