import streamlit as st
import requests
import os
import time

# --- CONFIGURATION ---
API_TOKEN = os.environ.get("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"

st.set_page_config(layout="wide", page_title="AI Notes Summarizer")

# --- API FUNCTION ---
def query_api(payload):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 503:
        estimated_time = response.json().get("estimated_time", 20)
        st.info(f"Model is loading, please wait about {int(estimated_time)} seconds...")
        time.sleep(estimated_time)
        response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# --- APP INTERFACE ---
st.title("🚀 AI Notes Summarizer (Cloud Powered)")
st.markdown("This version uses a cloud AI model, so it's much lighter and faster!")
user_text = st.text_area("👇 Paste your text here:", height=250, placeholder="Paste your long notes here...")

if st.button("Summarize Notes", type="primary"):
    if not user_text.strip():
        st.warning("⚠️ Please enter some text to summarize.")
    elif not API_TOKEN:
        st.error("❌ Hugging Face API token not found. Please add it to your Replit Secrets.")
    else:
        with st.spinner("AI is analyzing your notes... This might take a moment the first time."):
            summary_output = query_api({"inputs": user_text})
            if isinstance(summary_output, list) and 'summary_text' in summary_output[0]:
                summary = summary_output[0]['summary_text']
                st.success("✅ Summary Generated!")
                st.write(summary)
            else:
                if isinstance(summary_output, dict):
                    error_message = summary_output.get("error", "An unknown error occurred.")
                    st.error(f"Sorry, there was an error from the API: {error_message}")
                else:
                    st.error("Received an unexpected response from the API.")

