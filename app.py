"""
AI Data Analyst for SMBs - FIXED "Highest Balance" = SINGLE Customer!
"customer with highest balance" → 1 name + amount exactly!
"""

import streamlit as st
import pandas as pd
import numpy as np
from collections import defaultdict, Counter
import plotly.express as px
import plotly.graph_objects as go

# =============================================================================
# LEARNING ENGINE - ADMIN ONLY
# =============================================================================
@st.cache_data
def init_learning_engine():
    return {
        "patterns": 7, "new_keywords": [], "query_frequency": defaultdict(int),
        "success_patterns": defaultdict(int), "total_queries": 0, "successful_queries": 0,
        "success_rate": 0.75
    }

def learn_from_query(query, success=True):
    engine = st.session_state.learning_engine
    engine["total_queries"] += 1
    if success: engine["successful_queries"] += 1
    
    words = query.lower().split()
    business_words = [w for w in words if len(w) > 3 and w not in ['show', 'get', 'find', 'top', 'all', 'list']]
    
    new_words = [w for w in business_words if w not in engine["new_keywords"]]
    if new_words:
        engine["new_keywords"].extend(new_words)
        engine["patterns"] += len(new_words)
    
    for word in business_words:
        engine["query_frequency"][word] += 1
    
    prev_rate = engine["success_rate"]
    engine["success_rate"] = prev_rate * 0.9 + (1.0 if success else 0.0) * 0.1

# =============================================================================
# ADMIN PANEL
# =============================================================================
def show_admin_panel():
    st.sidebar.markdown("### 🔐 **ADMIN PANEL**"); st.sidebar.markdown("─" * 40)
    engine = st.session_state.learning_engine
    
    col1, col2, col3 = st.sidebar.columns(3)
    with col1: st.metric("🧠 Patterns", engine["patterns"])
    with col2: st.metric("✨ Keywords", len(engine["new_keywords"]))
    with col3: st.metric("📊 Success", f"{engine['success_rate']:.1%}")
    
    col4, col5 = st.sidebar.columns(2)
    with col4: st.metric("📈 Queries", engine["total_queries"])
    with col5: st.metric("✅ Success", engine["successful_queries"])
    
    st.sidebar.markdown("─" * 40); st.sidebar.markdown("### 🔥 **Top Patterns**")
    top_keywords = Counter(engine["query_frequency"]).most_common(5)
    for i, (keyword, count) in enumerate(top_keywords, 1):
        st.sidebar.markdown(f"{i}. **{keyword.title()}**: {count}")

# =============================================================================
# FIXED ANALYSIS - SINGLE CUSTOMER FOR "HIGHEST BALANCE"!
# =============================================================================
def find_best_numeric_column(df, keywords=[]):
    """Smart money column detection"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    money_keywords = ['balance', 'revenue', 'sales', 'amount', 'price', 'gst']
    
    best_col = None; best_score = 0
    for col in numeric_cols:
        score = sum(10 for keyword in money_keywords + keywords if keyword in col.lower())
        if score > best_score:
            best_score = score
            best_col = col
    
    if best_score == 0 and numeric_cols:
        col_values = [(col, df[col].sum()) for col in numeric_cols if df[col].sum() > 0]
        if col_values: best_col = max(col_values, key=lambda x: x[1])[0]
    
    return best_col

def find_customer_name(df, row_index):
    """Smart customer name detection"""
    name_cols = [col for col in df.columns if col.lower() in ['name', 'customer', 'user', 'id', 'subscriber']]
    if name_cols:
        return df.loc[row_index, name_cols[0]]
    return f"Customer {row_index}"

def analyze_data(df, query):
    query_lower = query.lower()
    
    # 🎯 FIXED: "customer with highest balance" = SINGLE customer!
    if 'customer' in query_lower and any(word in query_lower for word in ['highest', 'top', 'max']):
        value_col = find_best_numeric_column(df)
        
        if value_col and value_col in df.columns:
            # SINGLE TOP CUSTOMER (not top 10!)
            valid_data = df[[value_col]].dropna()
            if not valid_data.empty:
                top_row = valid_data.nlargest(1, value_col).iloc[0]
                top_value = top_row[value_col]
                customer_name = find_customer_name(df, top_row.name)
                
                # SINGLE customer card + mini chart
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown(f"""
                    ### 🏆 **#{1} Customer**
                    **{customer_name}**
                    **₹{top_value:,.0f}** {value_col.title()}
                    """)
                
                with col2:
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=[top_value], y=[customer_name],
                        orientation='h', text=[f'₹{top_value:,.0f}'],
                        textposition='outside',
                        marker_color='gold'
                    ))
                    fig.update_layout(
                        title=f"Top {value_col.title()}",
                        height=150, showlegend=False,
                        margin=dict(l=20, r=20, t=50, b=20)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                return f"✅ **{customer_name}** has highest **{value_col}**: ₹{top_value:,.0f}", fig
        
        return "❌ No customer data found", None
    
    # Top 10 (when NO "customer" keyword)
    elif any(word in query_lower for word in ['highest', 'top', 'max']):
        value_col = find_best_numeric_column(df)
        if value_col and value_col in df.columns:
            valid_data = df[[value_col]].dropna().nlargest(10, value_col)
            if not valid_data.empty:
                labels = [find_customer_name(df, idx) for idx in valid_data.index]
                fig = px.bar(
                    x=valid_data[value_col], y=labels, orientation='h',
                    title=f"🏆 Top 10 {value_col.title()}",
                    labels={value_col: value_col.title()},
                    color=valid_data[value_col], color_continuous_scale='Viridis'
                )
                fig.update_layout(height=400, showlegend=False)
                return f"✅ Top 10 **{value_col}** shown!", fig
        return "❌ No numeric data found", None
    
    # Totals
    elif any(word in query_lower for word in ['total', 'sum']):
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            totals = df[numeric_cols].sum()
            fig = px.bar(x=totals.values, y=totals.index, orientation='h',
                        title="💰 Column Totals", color=totals.values, color_continuous_scale='Blues')
            return "✅ Totals shown!", fig
        return "❌ No numeric data", None
    
    # Charts
    elif any(word in query_lower for word in ['chart', 'graph']):
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) >= 2:
            fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1],
                           title=f"{numeric_cols[0]} vs {numeric_cols[1]}")
            return "✅ Chart created!", fig
        return "❌ Need 2+ numeric columns", None
    
    return "📊 Try: 'customer with highest balance', 'top 10 revenue'", None

# =============================================================================
# MAIN APP
# =============================================================================
def main():
    st.set_page_config(page_title="AI Data Analyst", page_icon="🧠", layout="wide")
    
    st.title("🧠 **AI Data Analyst**"); st.markdown("*'customer with highest balance' → 1 customer instantly!*")
    
    if "learning_engine" not in st.session_state:
        st.session_state.learning_engine = init_learning_engine()
    if "df" not in st.session_state:
        st.session_state.df = None
    
    st.sidebar.title("⚙️ Controls")
    if st.sidebar.checkbox("🔐 **Admin Mode**"): show_admin_panel()
    
    uploaded_file = st.file_uploader("📁 **Upload CSV**", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file); st.session_state.df = df
        
        col1, col2 = st.columns([3, 1])
        with col1: 
            st.markdown("### 📊 **Data Preview**")
            st.dataframe(df.head(10), use_container_width=True)
        with col2:
            st.markdown("### 📈 **Stats**")
            st.metric("Rows", f"{len(df):,}")
            st.metric("Columns", len(df.columns))
            st.metric("Numeric", df.select_dtypes(include=[np.number]).shape[1])
        
        st.markdown("---")
        query = st.text_input("💬 **Ask:**", placeholder="customer with highest balance")
        
        if query:
            with st.spinner("🧠 Analyzing..."):
                result_text, chart = analyze_data(df, query)
                learn_from_query(query, success=chart is not None)
                
                st.markdown(result_text)
                if chart: st.plotly_chart(chart, use_container_width=True)
                else: st.info("💡 Try: 'customer with highest balance'")
    else:
        st.info("👆 **Upload CSV!**")
        st.markdown("""
        ### 🎯 **Works perfectly:**
        - `customer with highest balance` → **1 customer**
        - `top revenue` → **Top 10 list**
        - `total sales` → **Summary**
        """)

if __name__ == "__main__":
    main()
