import streamlit as st
import requests
import json
import os

# Assuming your FastAPI is running on http://localhost:8000
FASTAPI_BASE_URL = "http://localhost:8000/api/v1/employees"

st.set_page_config(page_title="AI Staffing Assistant", layout="wide")
st.title("AI Staffing Assistant")

st.markdown("""
    This application helps you find the best employees by:
    *   **Intelligent Matching:** Leveraging an LLM to understand project requirements from text or documents.
    *   **Skill-based Search:** Allowing detailed searches based on job titles, skills, department, and availability.
    *   **Document Analysis:** Processing various document types (PDF, DOCX, TXT) to extract key staffing needs.
    *   **Optimized Recommendations:** Providing tailored employee recommendations to meet your project's demands.
""")

# --- LLM Interaction ---
st.sidebar.header("AI Staffing Assistant")
llm_query_text = st.sidebar.text_area("Enter your project requirements or query:", "Find me an available Data Analyst with Tableau skills.", height=150)
uploaded_file = st.sidebar.file_uploader("Or upload a project requirements document (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])

llm_button = st.sidebar.button("Get Staffing Recommendation")

if llm_button:
    if not llm_query_text and not uploaded_file:
        st.warning("Please enter some requirements or upload a document.")
    else:
        files = None
        if uploaded_file:
            # Save the uploaded file temporarily to send to FastAPI
            file_path = os.path.join("temp", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            files = {"file": (uploaded_file.name, open(file_path, "rb"), uploaded_file.type)}

        try:
            data = {"query": llm_query_text} if llm_query_text else {}
            response = requests.post(f"{FASTAPI_BASE_URL}/llm_query", data=data, files=files)
            response.raise_for_status()
            llm_response = response.json()
            st.subheader("Staffing Recommendation:")
            st.markdown(llm_response['response'])
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the FastAPI backend. Please ensure it is running.")
        except requests.exceptions.HTTPError as e:
            st.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
        finally:
            if files and "file" in files:
                # Close the file handle and remove the temporary file
                files["file"][1].close()
                if os.path.exists(file_path):
                    os.remove(file_path)
