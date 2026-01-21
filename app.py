import sys
import os
import asyncio
# Add the parent directory to sys.path so we can import from backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from backend.github_client import fetch_issue_data
    from backend.ai_client import analyze_issue
except ImportError:
    st.error("Could not import backend modules. Make sure the 'backend' directory exists.")
    st.stop()

st.set_page_config(page_title="GitHub Issue Assistant", page_icon="🐞", layout="centered")

st.title("🐞 GitHub Issue Assistant")
st.markdown("Analyze GitHub issues with AI to understand, categorize, and prioritize them instantly.")

# Input Form
with st.form("issue_form"):
    repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/facebook/react")
    issue_number = st.number_input("Issue Number", min_value=1, step=1)
    submitted = st.form_submit_button("Analyze Issue")

async def process_issue(owner, repo, issue_num):
    # Fetch data
    issue_data = await fetch_issue_data(owner, repo, issue_num)
    # Analyze with AI
    analysis = analyze_issue(issue_data)
    return analysis

if submitted:
    if not repo_url:
        st.error("Please enter a repository URL.")
    else:
        with st.spinner("Fetching and analyzing issue..."):
            try:
                # Parse URL
                from urllib.parse import urlparse
                parsed_url = urlparse(repo_url)
                path_segments = parsed_url.path.strip("/").split("/")
                if len(path_segments) < 2:
                    raise ValueError("Invalid GitHub Repository URL")
                
                owner = path_segments[-2]
                repo = path_segments[-1]
                if repo.endswith(".git"):
                    repo = repo[:-4]

                # Run logic directly
                # We need a new loop or use asyncio.run if not in an existing loop
                # Streamlit runs in a separate thread, usually, but often no loop.
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                # If there's already a running loop (unlikely in standard script run but possible), use create_task
                # Ideally, just run_until_complete
                
                data = loop.run_until_complete(process_issue(owner, repo, issue_number))
                
                # Display Results
                st.success("Analysis Complete!")
                
                # Convert pydantic model to dict if needed, or access attributes directly
                # The model is IssueAnalysis
                
                st.subheader(data.summary)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Type**<br>{data.type.replace('_', ' ').title()}", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"**Priority**<br>{data.priority_score}", unsafe_allow_html=True)
                with col3:
                    st.write("**Labels**")
                    st.write(", ".join([f"`{label}`" for label in data.suggested_labels]))
                

                
                st.markdown("### Potential Impact")
                st.warning(data.potential_impact)
                    
            except ValueError as e:
                st.error(f"Error: {str(e)}")
            except Exception as e:
                import traceback
                st.error(f"An unexpected error occurred: {str(e)}")
                st.expander("Details").code(traceback.format_exc())

# Footer
st.markdown("---")
st.caption("Powered by Groq & FastAPI (Embedded)")
