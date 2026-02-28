import streamlit as st
import pandas as pd
import numpy as np
from langchain_anthropic import ChatAnthropic
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.callbacks import StreamlitCallbackHandler
import os

st.set_page_config(page_title="Databro", layout="wide")

st.title("🏢 **Databro** - SMB Data Analyst AI")
st.markdown("Upload CSV → Ask questions → Get insights instantly!")

MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB

with st.sidebar:
    st.header("⚙️ Setup")
    # FIXED: Render Environment Variable only
    claude_api_key = os.getenv("ANTHROPIC_API_KEY")
    if not claude_api_key:
        st.error("🚫 Add **ANTHROPIC_API_KEY** to Render Environment Variables")
        st.markdown("""
        **Render Setup:**
        1. Dashboard → Environment tab
        2. Key: `ANTHROPIC_API_KEY`
        3. Value: `sk-ant-your-complete-key`
        """)
        st.stop()
    
    uploaded_file = st.file_uploader("📁 Upload CSV/Excel", type=['csv', 'xlsx'], 
                                   help="Sales, GST, finance data (max 200MB)")

@st.cache_resource
def load_claude():
    return ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0,
        api_key=claude_api_key,
        streaming=True
    )

if uploaded_file is not None:
    if uploaded_file.size > MAX_FILE_SIZE:
        st.error("❌ File too large! Max **200MB**")
        st.stop()
    
    with st.spinner("🔄 Loading your data..."):
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
    
    with col2:
        st.subheader("📈 Quick Stats")
        st.metric("Total Records", f"{len(df):,}")
        st.metric("Columns", len(df.columns))
        st.metric("Missing Values", df.isnull().sum().sum())
    
    st.success("✅ Data loaded! Ask questions below 👇")
    st.info("🛡️ **Your data is secure**: Never stored, deleted after session")
    
    st.subheader("💬 Ask about your data")
    
    llm = load_claude()
    agent = create_pandas_dataframe_agent(
        llm, df,
        verbose=True,
        allow_dangerous_code=True,
        handle_parsing_errors=True,
        max_iterations=5
    )
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask anything... (ex: 'top 5 customers', 'sales trends')"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container())
            with st.spinner("🤖 Claude is analyzing your data..."):
                try:
                    response = agent.run(prompt, callbacks=[st_cb])
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("💡 Try simpler questions:\n• 'show top customers'\n• 'sales by month'\n• 'total revenue'")

else:
    st.info("👆 **Upload CSV/Excel to start analyzing**")
    st.markdown("""
    ### 🎯 **Perfect for SMBs** - Try these questions:
    ```
    💰 "Top 5 customers by revenue"
    📈 "Monthly sales trends" 
    🗺️ "Sales by region"
    📊 "Profit margins by product"
    ⚠️ "Find expense outliers"
    ```
    **200MB limit** = Full GST returns + FY data!
    """)

st.markdown("---")
st.markdown("""
💰 **₹499/month** | Built for Indian SMBs | Bank-grade security  
**Perfect for:** GST analysis, sales trends, expense tracking
""")
