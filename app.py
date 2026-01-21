import streamlit as st
import httpx
import os
from pydantic import ValidationError

st.set_page_config(page_title="GitHub Issue Assistant", page_icon="🐞", layout="centered")

st.title("🐞 GitHub Issue Assistant")
st.markdown("Analyze GitHub issues with AI to understand, categorize, and prioritize them instantly.")

# Input Form
with st.form("issue_form"):
    repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/facebook/react")
    issue_number = st.number_input("Issue Number", min_value=1, step=1)
    submitted = st.form_submit_button("Analyze Issue")

if submitted:
    if not repo_url:
        st.error("Please enter a repository URL.")
    else:
        with st.spinner("Fetching and analyzing issue..."):
            try:
                # Call Backend API
                api_url = os.getenv("API_URL", "http://127.0.0.1:8000").rstrip("/") + "/analyze"
                payload = {
                    "repo_url": repo_url,
                    "issue_number": issue_number
                }
                
                response = httpx.post(api_url, json=payload, timeout=30.0)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Display Results
                    st.success("Analysis Complete!")
                    
                    st.subheader(data["summary"])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"**Type**<br>{data['type'].replace('_', ' ').title()}", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"**Priority**<br>{data['priority_score']}", unsafe_allow_html=True)
                    with col3:
                        st.write("**Labels**")
                        st.write(", ".join([f"`{label}`" for label in data["suggested_labels"]]))
                    

                    
                    st.markdown("### Potential Impact")
                    st.warning(data["potential_impact"])
                    
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            
            except httpx.ConnectError:
                st.error("Could not connect to the backend server. Is it running?")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")

# Footer
st.markdown("---")
st.caption("Powered by Groq & FastAPI")
