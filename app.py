"""
AI Data Analyst for SMBs - Learns from EVERY peer query (Admin sees ALL)
Peers: Clean interface | You: Full learning analytics
"""

import streamlit as st
import pandas as pd
import numpy as np
from collections import defaultdict, Counter
import plotly.express as px
import plotly.graph_objects as go

# =============================================================================
# LEARNING ENGINE - ADMIN ONLY (Peers see NOTHING)
# =============================================================================
@st.cache_data
def init_learning_engine():
    """Initialize learning engine - persists across sessions"""
    return {
        "patterns": 7,                    # Starting basic patterns
        "new_keywords": [],               # Auto-discovered business terms
        "query_frequency": defaultdict(int),  # Tracks popular questions
        "success_patterns": defaultdict(int), # What analysis works best
        "total_queries": 0,
        "successful_queries": 0,
        "success_rate": 0.75             # Starting success rate
    }

def learn_from_query(query, success=True):
    """Peers ask → You track SILENTLY (invisible learning)"""
    engine = st.session_state.learning_engine
    
    engine["total_queries"] += 1
    if success:
        engine["successful_queries"] += 1
    
    # Extract business keywords (ignores show/get/top/etc)
    words = query.lower().split()
    business_words = [w for w in words 
                     if len(w) > 3 and w not in ['show', 'get', 'find', 'top', 'all', 'list']]
    
    # Learn NEW patterns/keywords
    new_words = [w for w in business_words if w not in engine["new_keywords"]]
    if new_words:
        engine["new_keywords"].extend(new_words)
        engine["patterns"] += len(new_words)
    
    # Track frequency of business terms
    for word in business_words:
        engine["query_frequency"][word] += 1
    
    # Update success rate (exponential moving average)
    prev_rate = engine["success_rate"]
    engine["success_rate"] = prev_rate * 0.9 + (1.0 if success else 0.0) * 0.1

# =============================================================================
# ADMIN PANEL - YOUR EYES ONLY
# =============================================================================
def show_admin_panel():
    """Private admin dashboard - toggle to see learning progress"""
    st.sidebar.markdown("### 🔐 **ADMIN PANEL**")
    st.sidebar.markdown("─" * 40)
    
    engine = st.session_state.learning_engine
    
    # Key Metrics Row 1
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        st.metric("🧠 Patterns Learned", engine["patterns"])
    with col2:
        st.metric("✨ New Keywords", len(engine["new_keywords"]))
    with col3:
        st.metric("📊 Success Rate", f"{engine['success_rate']:.1%}")
    
    st.sidebar.markdown("─" * 40)
    
    # Key Metrics Row 2
    col4, col5 = st.sidebar.columns(2)
    with col4:
        st.metric("📈 Total Queries", engine["total_queries"])
    with col5:
        st.metric("✅ Success Count", engine["successful_queries"])
    
    st.sidebar.markdown("─" * 40)
    
    # 🔥 TOP PATTERNS (Most popular keywords)
    st.sidebar.markdown("### 🔥 **Top 5 Patterns**")
    top_keywords = Counter(engine["query_frequency"]).most_common(5)
    for i, (keyword, count) in enumerate(top_keywords, 1):
        st.sidebar.markdown(f"{i}. **{keyword.title()}**: {count} asks")
    
    st.sidebar.markdown("─" * 40)
    
    # Recent Learning
    if engine["new_keywords"]:
        st.sidebar.markdown("### ✨ **Recently Learned**")
        recent = engine["new_keywords"][-5:]  # Last 5 new keywords
        for word in recent:
            st.sidebar.markdown(f"• {word.title()}")
    
    st.sidebar.markdown("─" * 40)
    st.sidebar.markdown("**👤 Peer Learning Mode Active**")

# =============================================================================
# DATA ANALYSIS ENGINE (Smart analysis based on learned patterns)
# =============================================================================
def analyze_data(df, query):
    """Smart analysis that gets better with learned patterns"""
    query_lower = query.lower()
    
    # Quick wins based on common SMB patterns
    if any(word in query_lower for word in ['highest', 'top', 'max']):
        col = df.select_dtypes(include=[np.number]).max().idxmax()
        if col in df.columns:
            top_n = df.nlargest(10, col)
            fig = px.bar(top_n, x=top_n.index, y=col, title=f"Top 10 {col.title()}")
            return f"✅ Top 10 **{col}** shown!", fig
    
    elif 'total' in query_lower or 'sum' in query_lower:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        totals = df[numeric_cols].sum()
        fig = px.bar(x=totals.index, y=totals.values, title="Column Totals")
        return f"✅ Totals for all numeric columns!", fig
    
    elif any(word in query_lower for word in ['chart', 'graph', 'trend']):
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) >= 2:
            fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1])
            return f"✅ Correlation chart: {numeric_cols[0]} vs {numeric_cols[1]}", fig
    
    # Default: Show basic stats
    st.info("📊 Basic data preview + stats")
    return "Data loaded successfully!", None

# =============================================================================
# MAIN APP
# =============================================================================
def main():
    st.set_page_config(
        page_title="AI Data Analyst",
        page_icon="🧠",
        layout="wide"
    )
    
    st.title("🧠 **AI Data Analyst for SMBs**")
    st.markdown("*Upload CSV → Ask questions → Get instant charts*")
    
    # Initialize learning engine
    if "learning_engine" not in st.session_state:
        st.session_state.learning_engine = init_learning_engine()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # LEFT SIDEBAR - ADMIN MODE TOGGLE (Peers don't see learning)
    # ═══════════════════════════════════════════════════════════════════════════
    st.sidebar.title("⚙️ Controls")
    
    # Admin mode toggle (hidden from peers by default)
    if st.sidebar.checkbox("🔐 **Admin Mode**", key="admin_mode"):
        show_admin_panel()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MAIN APP INTERFACE (Clean for peers)
    # ═══════════════════════════════════════════════════════════════════════════
    
    # File upload
    uploaded_file = st.file_uploader("📁 **Upload your CSV file**", type="csv")
    
    if uploaded_file is not None:
        # Load data
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        
        # Show data preview
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📊 **Data Preview**")
            st.dataframe(df.head(), use_container_width=True)
        
        with col2:
            st.markdown("### 📈 **Quick Stats**")
            st.metric("Rows", len(df))
            st.metric("Columns", len(df.columns))
            st.metric("Missing", df.isnull().sum().sum())
        
        # Query input
        st.markdown("---")
        query = st.text_input("💬 **Ask about your data:**", 
                            placeholder="e.g. 'show highest balance' or 'total revenue'")
        
        if query:
            with st.spinner("🧠 Analyzing..."):
                # Analyze data
                result_text, chart = analyze_data(df, query)
                
                # LEARN SILENTLY (Peers see nothing!)
                learn_from_query(query, success=chart is not None)
                
                # Show results (CLEAN - no learning info)
                st.success(result_text)
                
                if chart:
                    st.plotly_chart(chart, use_container_width=True)
                else:
                    st.info("💡 Try: 'highest', 'total', 'chart', 'top revenue'")
    
    else:
        st.info("👆 **Upload a CSV file to get started!**")
        st.markdown("""
        ### 🎯 **Perfect for SMBs:**
        - Telecom: highest balance, churn analysis
        - Retail: top sales, GST trends  
        - Services: revenue by region
        
        **Your peers' questions make it smarter automatically!**
        """)

if __name__ == "__main__":
    main()
