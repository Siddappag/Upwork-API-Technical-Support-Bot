"""
Streamlit Application
Web UI for Upwork API Technical Support Bot
"""

import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag import RAGBot

# Page configuration
st.set_page_config(
    page_title="Upwork API Technical Support Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5em;
        font-weight: bold;
        color: #14A800;
        margin-bottom: 10px;
    }
    .subheader {
        color: #555555;
        margin-bottom: 20px;
    }
    .answer-box {
        background-color: #1a1a1a;
        color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #14A800;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        font-size: 1.05em;
        line-height: 1.6;
    }
    .source-box {
        background-color: #F1F8E9;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 3px solid #558B2F;
    }
    .latency-box {
        background: linear-gradient(135deg, #FFD54F 0%, #FFC107 100%);
        padding: 16px;
        border-radius: 8px;
        text-align: center;
        margin: 20px 0;
        border-left: 5px solid #FF6F00;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        font-weight: bold;
        font-size: 1.1em;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'rag_bot' not in st.session_state:
    with st.spinner("Initializing RAG Bot..."):
        try:
            st.session_state.rag_bot = RAGBot()
        except Exception as e:
            st.error(f"Failed to initialize RAG Bot: {str(e)}")
            st.stop()

# Header
st.markdown('<div class="main-header">🤖 Upwork API Technical Support Bot</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Ask questions about the Upwork API documentation</div>', unsafe_allow_html=True)

# Sidebar info
with st.sidebar:
    st.markdown("### About")
    st.markdown("""
    This is a **RAG-powered AI assistant** that answers questions about the Upwork API documentation.
    
    **Features:**
    - 📚 Retrieves relevant documentation
    - 🧠 Uses DeepInfra's Meta-Llama 3.1 model
    - 🔒 No hallucinations - only answers from documentation
    - ⚡ Shows response latency
    
    **How it works:**
    1. Your question is embedded
    2. Similar documentation chunks are retrieved
    3. LLM generates answer from context
    4. Sources are displayed
    """)
    
    st.markdown("---")
    st.markdown("### Vector Database Status")
    try:
        collection_size = st.session_state.rag_bot.vector_store.get_collection_size()
        st.success(f"✓ Documents loaded: {collection_size}")
    except:
        st.error("Vector database not initialized. Run ingest.py first.")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Ask a Question")

user_query = st.text_input(
    label="Enter your question about Upwork API:",
    placeholder="e.g., What is the OAuth access token validity period?",
    key="user_query"
)

ask_button = st.button("🔍 Ask Question", type="primary", use_container_width=True)

if ask_button and user_query.strip():
    with st.spinner("🔄 Processing your question..."):
        try:
            answer, sources, response_time = st.session_state.rag_bot.answer_question(user_query)
            
            # Display answer
            st.markdown("### 📝 Answer")
            st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)
            
            # Display response latency prominently
            col_time, col_blank = st.columns([1, 2])
            with col_time:
                st.metric("Response Time", f"{response_time:.2f}s", delta=None, delta_color="off")
            
            # Display sources
            st.markdown("### 📚 Sources")
            
            if sources:
                for i, source in enumerate(sources, 1):
                    with st.expander(f"Source {i}"):
                        st.text(source)
            else:
                st.warning("No relevant documentation found for your query.")
        
        except Exception as e:
            st.error(f"Error processing query: {str(e)}")

elif ask_button:
    st.warning("Please enter a question first.")

# Evaluation section
with st.expander("📋 Evaluation Questions"):
    st.markdown("""
    Try asking these evaluation questions to test the bot:
    
    1. **Question:** What is the specific request-per-second rate limit for the Upwork API, and is it enforced per Key or per IP?
    
    2. **Question:** How long is an OAuth access token valid for?
       - **Expected Answer:** 24 hours
    
    3. **Question:** Can I use a Client Credentials Grant to access a user's private contract details?
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.8em;">
    Upwork API Technical Support Bot v1.0 | Powered by LangChain + DeepInfra
</div>
""", unsafe_allow_html=True)
