# streamlit_app.py
import streamlit as st
import requests
import json
from typing import List

# Page configuration
st.set_page_config(
    page_title="Doki - Chat with RamanSpy Docs",
    page_icon="🔬",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left-color: #9c27b0;
    }
    .stTextInput > div > div > input {
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.markdown('<h1 class="main-header">🔬 Doki - Chat with RamanSpy Documentation</h1>', unsafe_allow_html=True)

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This is a RAG-powered chat interface for the RamanSpy documentation.
    
    **Features:**
    - Ask questions about RamanSpy
    - Get answers from the documentation
    - Powered by vector search and LLM
    
    **API Status:** Check if the backend is running
    """)
    
    # API status check
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            st.success("✅ API is running")
        else:
            st.error("❌ API returned an error")
    except requests.exceptions.RequestException:
        st.error("❌ Cannot connect to API")
        st.info("Make sure the uvicorn server is running on port 8000")

# Main chat interface
st.header("💬 Chat with RamanSpy Docs")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about RamanSpy..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Make API request
            response = requests.post(
                "http://localhost:8000/chat",
                json={"question": prompt},
                timeout=30
            )
            
            if response.status_code == 200:
                answer = response.json()["answer"]
                message_placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                error_msg = f"API Error: {response.status_code} - {response.text}"
                message_placeholder.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Connection Error: {str(e)}"
            message_placeholder.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Clear chat button
if st.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# Example questions
st.header("💡 Example Questions")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("How to load data?"):
        st.session_state.messages.append({"role": "user", "content": "How do I load data in RamanSpy?"})
        st.rerun()

with col2:
    if st.button("Preprocessing steps"):
        st.session_state.messages.append({"role": "user", "content": "What are the preprocessing steps available in RamanSpy?"})
        st.rerun()

with col3:
    if st.button("Denoising methods"):
        st.session_state.messages.append({"role": "user", "content": "What denoising methods are available in RamanSpy?"})
        st.rerun()

# Footer
st.markdown("---")
st.markdown("🔬 **RamanSpy Documentation Chat** - Powered by RAG and Groq LLM") 