"""
🧠 DATABRO - AI Data Analyst with NLP
Natural queries: "top customers", "customer names", "highest revenue" ALL WORK!
"""

import streamlit as st
import pandas as pd
import numpy as np
from collections import defaultdict, Counter
import plotly.express as px
import plotly.graph_objects as go
import re

# =============================================================================
# SIMPLE NLP - No external libraries needed!
# =============================================================================
def databro_nlp_parse(query):
    """NLP: Converts natural language → structured intent"""
    query_lower = query.lower()
    
    # Intent detection
    if re.search(r'(top|best|highest|leading).*?(customer|client|user)', query_lower):
        n_match = re.search(r'top\s+(\d+)', query_lower)
        return {'intent': 'top_n_customers', 'n': int(n_match.group(1)) if n_match else 5}
    
    if re.search(r'(name|list).*?(customer|client|user)', query_lower):
        return {'intent': 'list_customers'}
    
    if re.search(r'(user|customer).*?(highest|top|best|maximum)', query_lower):
        return {'intent': 'single_top_customer'}
    
    if re.search(r'(total|sum|overall).*?(revenue|sales|balance|amount)', query_lower):
        return {'intent': 'totals'}
    
    if re.search(r'(chart|graph|visual|plot)', query_lower):
        return {'intent': 'chart'}
    
    # Column extraction
    money_cols = ['revenue', 'sales', 'balance', 'amount', 'price', 'gst']
    for col in money_cols:
        if col in query_lower:
            return {'intent': 'analyze_column', 'column': col}
    
    return {'intent': 'general_analysis'}

def find_best_numeric_column(df, keywords=[]):
    """Smart money column detection"""
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

def find_customer_name_column(df):
    """Smart customer name detection"""
    name_keywords = ['name', 'customer', 'user', 'id', 'subscriber', 'client']
    for col in df.columns:
        if any(keyword in col.lower() for keyword in name_keywords):
            return col
    return df.columns[0] if len(df.columns) > 0 else None

def find_customer_name(df, row_index, name_col=None):
    if name_col is None:
        name_col = find_customer_name_column(df)
    if name_col and name_col in df.columns:
        try:
            val = df.loc[row_index, name_col]
            return str(val) if pd.notna(val) else f"Row {row_index}"
        except:
            return f"Row {row_index}"
    return f"Row {row_index}"

# =============================================================================
# DATABRO LEARNING ENGINE
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
# DATABRO ADMIN PANEL
# =============================================================================
def show_databro_admin():
    st.sidebar.markdown("### 🔐 **DATABRO ADMIN**")
    st.sidebar.markdown("─" * 30)
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
# DATABRO NLP ANALYSIS ENGINE
# =============================================================================
def databro_analyze(df, query):
    parsed = databro_nlp_parse(query)
    wants_chart = any(word in query.lower() for word in ['chart', 'graph', 'plot', 'visual'])
    
    # 🎯 LIST CUSTOMERS
    if parsed['intent'] == 'list_customers':
        name_col = find_customer_name_column(df)
        if name_col:
            customer_names = df[name_col].dropna().unique()
            if len(customer_names) > 0:
                table_data = [{"#": i+1, "Customer": name} for i, name in enumerate(customer_names[:10])]
                df_table = pd.DataFrame(table_data)
                
                st.markdown(f"✅ **Customer Names** (from **{name_col}**) - **{len(customer_names):,} total**")
                st.dataframe(df_table, use_container_width=True, hide_index=True)
                
                if len(customer_names) > 10:
                    st.info(f"💡 Showing first 10 of {len(customer_names):,} customers")
                
                return f"✅ Found **{len(customer_names):,} unique customers**", None
        return "❌ No customer column found", None
    
    # 🎯 TOP N CUSTOMERS
    elif parsed['intent'] == 'top_n_customers':
        value_col = find_best_numeric_column(df)
        if value_col:
            valid_data = df[[value_col]].dropna().nlargest(parsed['n'], value_col)
            if not valid_data.empty:
                name_col = find_customer_name_column(df)
                table_data = []
                for i, idx in enumerate(valid_data.index, 1):
                    name = find_customer_name(df, idx, name_col)
                    amount = valid_data.loc[idx, value_col]
                    table_data.append({"#": i, "Customer": name, value_col: f"₹{amount:,.0f}"})
                
                df_table = pd.DataFrame(table_data)
                st.markdown(f"✅ **Top {parsed['n']} {value_col.title()}**")
                st.dataframe(df_table, use_container_width=True, hide_index=True)
                
                if wants_chart:
                    labels = [row['Customer'] for row in table_data]
                    values = [float(v.replace('₹', '').replace(',', '')) for v in [row[value_col] for row in table_data]]
                    fig = px.bar(x=values, y=labels, orientation='h', title=f"Top {parsed['n']}",
                               color=values, color_continuous_scale='Viridis')
                    fig.update_layout(height=300, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                    return f"✅ Top {parsed['n']} table + chart", fig
                return f"✅ Top {parsed['n']} customers", None
        return "❌ No numeric data", None
    
    # 🎯 SINGLE TOP CUSTOMER
    elif parsed['intent'] == 'single_top_customer':
        value_col = find_best_numeric_column(df)
        if value_col:
            valid_data = df[[value_col]].dropna()
            if not valid_data.empty:
                top_row = valid_data.nlargest(1, value_col).iloc[0]
                name_col = find_customer_name_column(df)
                customer_name = find_customer_name(df, top_row.name, name_col)
                response = f"✅ **{customer_name}** has highest **{value_col}**: **₹{top_row[value_col]:,.0f}**"
                
                if wants_chart:
                    fig = go.Figure()
                    fig.add_trace(go.Bar(x=[top_row[value_col]], y=[customer_name], orientation='h',
                                       text=[f'₹{top_row[value_col]:,.0f}'], textposition='outside',
                                       marker_color='#FFD700'))
                    fig.update_layout(height=120, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                    return response, fig
                return response, None
        return "❌ No customer data", None
    
    # 🎯 TOTALS
    elif parsed['intent'] == 'totals':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            totals = df[numeric_cols].sum()
            response = f"✅ **Grand Total**: ₹{totals.sum():,.0f}\n"
            for col in totals.index:
                response += f"• **{col}**: ₹{totals[col]:,.0f}\n"
            if wants_chart:
                fig = px.bar(x=totals.values, y=totals.index, orientation='h',
                           title="Totals", color=totals.values, color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)
                return response, fig
            return response, None
        return "❌ No numeric data", None
    
    # Default analysis
    value_col = find_best_numeric_column(df)
    if value_col:
        valid_data = df[[value_col]].dropna().nlargest(5, value_col)
        name_col = find_customer_name_column(df)
        top_3 = [find_customer_name(df, idx, name_col) for idx in valid_data.head(3).index]
        return f"✅ **Top 3 {value_col}**:\n• **{top_3[0]}** (1st)\n• **{top_3[1]}** (2nd)\n• **{top_3[2]}** (3rd)", None
    
    return "💡 **Databro understands**: 'top customers', 'customer names', 'highest revenue user', 'total sales'", None

# =============================================================================
# DATABRO MAIN CHAT
# =============================================================================
def main():
    st.title("🧠 **Databro** - NLP Data Analyst")
    st.markdown("**💬 Natural language works! 'top customers by revenue' → Perfect table!**")
    
    if "learning_engine" not in st.session_state:
        st.session_state.learning_engine = init_learning_engine()
    if "df" not in st.session_state:
        st.session_state.df = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    st.sidebar.title("⚙️ **Databro Controls**")
    if st.sidebar.checkbox("🔐 **Databro Admin**"):
        show_databro_admin()
    
    uploaded_file = st.file_uploader("📁 **Upload CSV**", type="csv")
    
    if uploaded_file is not None and st.session_state.df is None:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        st.success("✅ **Databro loaded your data with NLP!** Ask naturally 👇")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 📊 **Data Preview**")
            st.dataframe(df.head(10), use_container_width=True)
        with col2:
            st.markdown("### 📈 **Databro Stats**")
            st.metric("Rows", f"{len(df):,}")
            st.metric("Columns", len(df.columns))
    
    st.markdown("─" * 80)
    
    if st.session_state.chat_history:
        st.markdown("### 💬 **Databro Chat**")
        for query, response in st.session_state.chat_history[-5:]:
            with st.chat_message("user"):
                st.write(f"**You**: {query}")
            with st.chat_message("assistant"):
                st.markdown(response)
    
    if st.session_state.df is not None:
        st.markdown("### 🤖 **Chat with Databro**")
        query = st.chat_input("Try: 'top customers', 'name of customer', 'highest revenue user'...")
        
        if query:
            with st.chat_message("user"):
                st.write(f"**You**: {query}")
            
            with st.chat_message("assistant"):
                with st.spinner("Databro analyzing with NLP..."):
                    result_text, chart = databro_analyze(st.session_state.df, query)
                    learn_from_query(query, success=result_text != "❌")
                    
                    st.session_state.chat_history.append((query, result_text))
                    
                    if result_text and result_text != "❌":
                        st.success(result_text)
                    else:
                        st.warning(result_text)
    else:
        st.info("👆 **Upload CSV → Chat naturally with Databro NLP!**")
        st.markdown("""
        ### 🎯 **Databro NLP Examples:**
        • `top customers by revenue` → **Smart table**
        • `name of customer` → **All names**
        • `highest revenue user` → **Single answer**
        • `show total sales chart` → **Visual**
        """)

if __name__ == "__main__":
    main()
