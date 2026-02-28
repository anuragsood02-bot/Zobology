"""
AI Data Analyst - Top N Tables + Text + Charts!
"top 3 balance" → Table | "user with highest" → Text | "chart" → Visual
"""

import streamlit as st
import pandas as pd
import numpy as np
from collections import defaultdict, Counter
import plotly.express as px
import plotly.graph_objects as go
import re

# =============================================================================
# LEARNING ENGINE - Admin Only
# =============================================================================
@st.cache_data
def init_learning_engine():
    return {
        "patterns": 7, "new_keywords": [], "query_frequency": defaultdict(int),
        "total_queries": 0, "successful_queries": 0, "success_rate": 0.75
    }

def learn_from_query(query, success=True):
    engine = st.session_state.learning_engine
    engine["total_queries"] += 1
    if success: engine["successful_queries"] += 1
    
    words = query.lower().split()
    business_words = [w for w in words if len(w) > 3 and w not in ['show','get','find','top','all','list']]
    
    new_words = [w for w in business_words if w not in engine["new_keywords"]]
    if new_words:
        engine["new_keywords"].extend(new_words)
        engine["patterns"] += len(new_words)
    
    for word in business_words:
        engine["query_frequency"][word] += 1
    
    engine["success_rate"] = engine["success_rate"] * 0.9 + (1.0 if success else 0.0) * 0.1

# =============================================================================
# ADMIN PANEL
# =============================================================================
def show_admin_panel():
    st.sidebar.markdown("### 🔐 **ADMIN**"); st.sidebar.markdown("─" * 30)
    engine = st.session_state.learning_engine
    
    col1, col2, col3 = st.sidebar.columns(3)
    with col1: st.metric("🧠 Patterns", engine["patterns"])
    with col2: st.metric("✨ Keywords", len(engine["new_keywords"]))
    with col3: st.metric("📊 Success", f"{engine['success_rate']:.0%}")
    
    st.sidebar.markdown("### 🔥 **Top Patterns**")
    top_keywords = Counter(engine["query_frequency"]).most_common(5)
    for i, (keyword, count) in enumerate(top_keywords, 1):
        st.sidebar.markdown(f"{i}. **{keyword}**: {count}")

# =============================================================================
# SMART ANALYSIS - Tables for Top N!
# =============================================================================
def extract_top_n(query):
    """Extract number from 'top 3', 'top 5', etc."""
    match = re.search(r'top\s+(\d+)', query.lower())
    return int(match.group(1)) if match else None

def find_best_numeric_column(df, keywords=[]):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    money_keywords = ['balance', 'revenue', 'sales', 'amount', 'price', 'gst', 'total']
    
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
    name_cols = [col for col in df.columns if any(k in col.lower() for k in ['name','customer','user','id','subscriber'])]
    if name_cols:
        val = df.loc[row_index, name_cols[0]]
        return val if pd.notna(val) else f"Row {row_index}"
    return f"Row {row_index}"

def analyze_data(df, query):
    query_lower = query.lower()
    wants_chart = any(word in query_lower for word in ['chart', 'graph', 'plot', 'visual'])
    top_n = extract_top_n(query)
    
    # 🎯 TOP N TABLE (top 3, top 5, top 10)
    if top_n:
        value_col = find_best_numeric_column(df)
        if value_col and value_col in df.columns:
            valid_data = df[[value_col]].dropna().nlargest(top_n, value_col)
            if not valid_data.empty:
                # Create table data
                table_data = []
                for idx in valid_data.index:
                    name = find_customer_name(df, idx)
                    amount = valid_data.loc[idx, value_col]
                    table_data.append({"Rank": len(table_data)+1, "Customer": name, value_col: f"₹{amount:,.0f}"})
                
                df_table = pd.DataFrame(table_data)
                
                response = f"✅ **Top {top_n} {value_col.title()}**"
                
                # Show table
                st.dataframe(df_table, use_container_width=True, hide_index=True)
                
                # Chart if requested
                if wants_chart:
                    labels = [row['Customer'] for row in table_data]
                    values = [float(v.replace('₹', '').replace(',', '')) for v in [row[value_col] for row in table_data]]
                    fig = px.bar(x=values, y=labels, orientation='h',
                               title=f"Top {top_n} {value_col.title()}", color=values,
                               color_continuous_scale='Viridis')
                    fig.update_layout(height=300, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                
                return response, None if not wants_chart else fig
            return f"❌ Not enough data for top {top_n}", None
        
        return "❌ No numeric data found", None
    
    # 🎯 SINGLE USER - Text only
    elif 'user' in query_lower and any(word in query_lower for word in ['highest','top','max']):
        value_col = find_best_numeric_column(df)
        if value_col and value_col in df.columns:
            valid_data = df[[value_col]].dropna()
            if not valid_data.empty:
                top_row = valid_data.nlargest(1, value_col).iloc[0]
                top_value = top_row[value_col]
                customer_name = find_customer_name(df, top_row.name)
                
                response = f"✅ **{customer_name}** has highest **{value_col}**: **₹{top_value:,.0f}**"
                
                if wants_chart:
                    fig = go.Figure()
                    fig.add_trace(go.Bar(x=[top_value], y=[customer_name], orientation='h',
                                       text=[f'₹{top_value:,.0f}'], textposition='outside',
                                       marker_color='#FFD700', marker_line_color='black', marker_line_width=2))
                    fig.update_layout(height=120, showlegend=False, margin=dict(t=10))
                    return response, fig
                return response, None
        
        return "❌ No user data found", None
    
    # Regular highest/top (no number) - Text summary
    elif any(word in query_lower for word in ['highest','top','max']):
        value_col = find_best_numeric_column(df)
        if value_col and value_col in df.columns:
            valid_data = df[[value_col]].dropna().nlargest(10, value_col)
            if not valid_data.empty:
                top_3_names = [find_customer_name(df, idx) for idx in valid_data.head(3).index]
                total_top10 = valid_data[value_col].sum()
                
                response = f"✅ Top **{value_col}**:\n• **{top_3_names[0]}** (#{1})\n• **{top_3_names[1]}** (#{2})\n• **{top_3_names[2]}** (#{3})\n... Top 10 total: **₹{total_top10:,.0f}**"
                
                if wants_chart:
                    labels = [find_customer_name(df, idx) for idx in valid_data.index]
                    fig = px.bar(x=valid_data[value_col], y=labels, orientation='h',
                               title=f"Top 10 {value_col.title()}", color=valid_data[value_col],
                               color_continuous_scale='Viridis')
                    fig.update_layout(height=400, showlegend=False)
                    return response, fig
                return response, None
        
        return "❌ No numeric data", None
    
    # Totals
    elif any(word in query_lower for word in ['total','sum']):
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            totals = df[numeric_cols].sum()
            total_all = totals.sum()
            response = f"✅ **Total**: ₹{total_all:,.0f}\n"
            for col in totals.index:
                response += f"• **{col}**: ₹{totals[col]:,.0f}\n"
            
            if wants_chart:
                fig = px.bar(x=totals.values, y=totals.index, orientation='h',
                           title="Totals", color=totals.values, color_continuous_scale='Blues')
                return response, fig
            return response, None
        return "❌ No numeric data", None
    
    return "💡 Try: 'top 3 balance', 'top 5 revenue', 'user with highest', 'total sales'", None

# =============================================================================
# MAIN APP
# =============================================================================
def main():
    st.set_page_config(page_title="AI Data Analyst", page_icon="🧠", layout="wide")
    
    st.title("🧠 **AI Data Analyst**")
    st.markdown("**Tables for 'top 3/5/10' | Text by default | Charts when asked**")
    
    if "learning_engine" not in st.session_state:
        st.session_state.learning_engine = init_learning_engine()
    if "df" not in st.session_state:
        st.session_state.df = None
    if "query_history" not in st.session_state:
        st.session_state.query_history = []
    
    st.sidebar.title("⚙️ Controls")
    if st.sidebar.checkbox("🔐 **Admin Mode**"): show_admin_panel()
    
    uploaded_file = st.file_uploader("📁 **Upload CSV**", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 📊 **Data Preview**")
            st.dataframe(df.head(10), use_container_width=True)
        with col2:
            st.markdown("### 📈 **Stats**")
            st.metric("Rows", f"{len(df):,}")
            st.metric("Columns", len(df.columns))
            st.metric("Numeric", df.select_dtypes(include=[np.number]).shape[1])
        
        st.markdown("─" * 80)
        
        st.markdown("### 💬 **Ask Questions**")
        query = st.text_input("", placeholder="top 3 balance, top 5 revenue, user with highest balance...",
                            key="main_query", label_visibility="collapsed")
        
        if query and st.session_state.df is not None:
            with st.spinner("🧠 Analyzing..."):
                result_text, chart = analyze_data(st.session_state.df, query)
                learn_from_query(query, success=result_text != "❌")
                
                if result_text:
                    st.markdown(result_text)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)
                
                st.session_state.query_history.append(query)
        
        if st.session_state.query_history:
            with st.expander("📜 Previous Questions"):
                for q in st.session_state.query_history[-3:]:
                    st.write(f"• {q}")
    
    else:
        st.info("👆 **Upload CSV!**")
        st.markdown("""
        ### 🎯 **Smart Responses:**
        • `top 3 balance` → **Clean table**
        • `top 5 revenue` → **Table format**  
        • `user with highest` → **Single name + amount**
        • `top revenue chart` → **Text + bar chart**
        """)

if __name__ == "__main__":
    main()
