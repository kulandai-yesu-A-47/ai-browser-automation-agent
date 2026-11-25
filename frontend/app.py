import streamlit as st
import requests

st.set_page_config(page_title="AI Browser Automation Agent", page_icon="🌐", layout="wide")
API_URL = "http://127.0.0.1:8000"

st.title("🌐 AI Browser Automation Agent")
st.caption("Give a task in plain English. The agent can search, open pages, read content and fill simple forms.")

with st.sidebar:
    st.subheader("Example tasks")
    st.markdown("""
    - Search for Python AI internships in Chennai
    - Open https://www.python.org and summarize the page
    - Read the current page content
    - Fill a form using the visible field labels
    """)
    st.warning("Safety: this demo does not submit forms, make purchases, send messages, or enter passwords.")

task = st.text_area("What should the browser do?", height=110,
                    placeholder="Example: Search for beginner Python tutorials and summarize the top results.")
if st.button("Run task", type="primary", disabled=not task.strip()):
    with st.spinner("Agent is working..."):
        try:
            response = requests.post(f"{API_URL}/agent/run", json={"task": task}, timeout=240)
            response.raise_for_status()
            data = response.json()
            st.subheader("Agent response")
            st.write(data.get("reply", "Task completed."))
            for index, step in enumerate(data.get("steps", []), 1):
                with st.expander(f"Step {index}: {step.get('action', 'action')}"):
                    result = step.get("result", {})
                    st.write("URL:", result.get("url", ""))
                    st.write("Title:", result.get("title", ""))
                    if result.get("filled_fields") is not None:
                        st.write("Filled fields:", ", ".join(result["filled_fields"]) or "No matching fields")
                    if result.get("text"):
                        st.text_area("Page content", result["text"], height=220, key=f"content_{index}")
                    if result.get("error"):
                        st.error(result["error"])
                    if result.get("message"):
                        st.info(result["message"])
        except requests.RequestException as exc:
            st.error(f"Could not connect to backend: {exc}. Make sure FastAPI is running.")
