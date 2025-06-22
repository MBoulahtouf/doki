# streamlit_app.py
import streamlit as st
import requests

# --- STREAMLIT PAGE SETUP ---
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

# Header
st.markdown('<h1 class="main-header">🔬 Doki - Chat with RamanSpy Documentation</h1>', unsafe_allow_html=True)

# --- API Configuration ---
API_URL = "http://127.0.0.1:8000/chat"

# Sidebar with information and API status
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This is a RAG-powered chat interface for the RamanSpy documentation.
    
    **Features:**
    - Ask questions about RamanSpy
    - Get answers from the documentation
    - Powered by vector search and LLM
    - **History-aware** - Follow-up questions work!
    
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

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if user_question := st.chat_input("Ask a question about RamanSpy..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_question})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_question)
    
    # Display assistant response with spinner
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Prepare chat history for the API
                chat_history = []
                for msg in st.session_state.messages[:-1]:  # Exclude the current question
                    if msg["role"] == "user":
                        chat_history.append({"role": "human", "content": msg["content"]})
                    elif msg["role"] == "assistant":
                        chat_history.append({"role": "ai", "content": msg["content"]})
                
                # Make API request with chat history
                response = requests.post(
                    API_URL, 
                    json={
                        "question": user_question,
                        "chat_history": chat_history
                    }, 
                    timeout=30
                )
                response.raise_for_status()  # Better error handling
                
                api_response = response.json()
                answer = api_response.get("answer", "Sorry, I couldn't get a valid answer from the server.")
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except requests.exceptions.RequestException as e:
                error_msg = f"An error occurred while connecting to the backend API: {e}"
                st.error(error_msg)
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