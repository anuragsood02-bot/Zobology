import streamlit as st
import pandas as pd
import numpy as np
from langchain_anthropic import ChatAnthropic
from langchain_experimental.agents import create_pandas_dataframe_agent  # FIXED IMPORT
from langchain.callbacks import StreamlitCallbackHandler
import os

# Set page config
st.set_page_config(page_title="Databro", layout="wide")

st.title("🏢 **Databro** - SMB Data Analyst AI")
st.markdown("Upload CSV → Ask questions → Get insights instantly! No data scientist needed!")

# SECURITY: File size limit (200MB)
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB

# Sidebar for setup
with st.sidebar:
    st.header("⚙️ Setup")
    
    # SECURITY: Use Streamlit secrets
    claude_api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    
    if not claude_api_key:
        st.error("🚫 Add **ANTHROPIC_API_KEY** to Render Environment")
        st.stop()
    
    uploaded_file = st.file_uploader("📁 Upload CSV/Excel", 
                                   type=['csv', 'xlsx'],
                                   help="Sales, finance, or ops data (max 200MB)")

# Initialize Claude LLM
@st.cache_resource
def load_claude():
    return ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
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
    
    # Load data
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
    
    st.in
