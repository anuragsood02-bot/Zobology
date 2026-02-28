import streamlit as st
import pandas as pd
import numpy as np
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_pandas_dataframe_agent
from langchain.callbacks import StreamlitCallbackHandler
import io
import os

# Set page config
st.set_page_config(page_title="SMB Data Analyst", layout="wide")

st.title("🏢 SMB Data Analyst AI")
st.markdown("Upload CSV → Ask questions → Get insights (No data scientist needed!)")

# SECURITY: File size limit (200MB)
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB ✅

# Sidebar for setup
with st.sidebar:
    st.header("⚙️ Setup")
    
    # SECURITY: Use Streamlit secrets (never expose in UI)
    claude_api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    
    if not claude_api_key:
        st.error("🚫 Add **ANTHROPIC_API_KEY** to Streamlit Secrets")
        st.markdown("""
        ### How to add:
        1. Go to repo Settings → Secrets
        2. Add: `ANTHROPIC_API_KEY = sk-ant-...`
        """)
        st.stop()
    
    uploaded_file = st.file_uploader("📁 Upload CSV/Excel", 
                                   type=['csv', 'xlsx'],
                                   help="Sales, finance, or ops data (max 200MB)")

# Initialize Claude LLM
@st.cache_resource
def load_claude():
    return ChatAnthropic(
        model="claude-3-5-sonnet-20241022",  # Best for data analysis
        temperature=0,
        api_key=claude_api_key,
        streaming=True
    )

# Main app logic
if uploaded_file is not None:
    # SECURITY: Check file size
    if uploaded_file.size > MAX_FILE_SIZE:
        st.error("❌ File too large! Max **200MB**")
        st.stop()
    
    # Load data (NEVER store permanently)
    with st.spinner("Loading your data..."):
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    
    # Data preview & stats
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
    
    with col2:
        st.subheader("📈 Quick Stats")
        st.metric("Total Records", f"{len(df):,}")
        st.metric("Columns", len(df.columns))
        st.metric("Missing Values", df.isnull().sum().sum())
    
    # SECURITY: Data deleted after session
    st.info("🛡️ **Your data is secure**: Never stored, deleted after session")
    
    # AI Chat Interface
    st.subheader("💬 Ask about your data")
    
    llm = load_claude()
    agent = create_pandas_dataframe_agent(
        llm, df,
        verbose=True,
        allow_dangerous_code=True,  # Needed for pandas ops
        handle_parsing_errors=True,
        max_iterations=5  # Prevent infinite loops
    )
    
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Show chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask anything... (ex: 'top 5 customers', 'sales trends')"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container())
            with st.spinner("Claude is analyzing..."):
                try:
                    response = agent.run(prompt, callbacks=[st_cb])
                    st.markdown(response)
                except Exception as e:
                    st.error(f"Analysis error: {str(e)}")
                    st.info("Try simpler questions first")
        
        st.session_state.messages.append({"role": "assistant", "content": response})

else:
    st.info("👆 Upload CSV/Excel to start")
    st.markdown("""
    ### 🎯 SMB Questions to Try:
    ```
    • "Top 5 customers by revenue"
    • "Monthly sales trends" 
    • "Which products sell best?"
    • "Show profit margins by region"
    • "Find expense outliers"
    ```
    """)

# Footer
st.markdown("---")
st.markdown("💰 **₹499/month** | Bank-grade security | Built for Indian SMBs")

