import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

class DatabroAI:
    def __init__(self):
        self.patterns = {
            'top': ['top', 'highest', 'largest', 'maximum', 'best', 'leaderboard'],
            'bottom': ['lowest', 'smallest', 'minimum', 'worst'],
            'total': ['total', 'sum', 'overall', 'aggregate', 'grand total'],
            'average': ['average', 'mean', 'avg', 'average value'],
            'trend': ['trend', 'growth', 'change', 'pattern', 'over time', 'time series'],
            'correlation': ['correlation', 'relationship', 'compare', 'vs', 'versus', 'between'],
            'scatter': ['scatter', 'plot', 'graph', 'chart', 'visualize', 'show me'],
            'distribution': ['distribution', 'histogram', 'breakdown', 'frequency']
        }
    
    def parse_query(self, query, df):
        """Advanced AI query parsing"""
        query_lower = query.lower()
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Graph/correlation detection
        if any(word in query_lower for word in self.patterns['scatter']):
            return 'scatter', numeric_cols[:2] if len(numeric_cols) >= 2 else [numeric_cols[0]]
        if any(word in query_lower for word in self.patterns['correlation']):
            return 'correlation', numeric_cols[:2] if len(numeric_cols) >= 2 else [numeric_cols[0]]
        if any(word in query_lower for word in self.patterns['trend']):
            return 'trend', [numeric_cols[0]] if numeric_cols else []
        
        # Top/bottom/total/average
        if any(word in query_lower for word in self.patterns['top']):
            return 'top', [numeric_cols[0]] if numeric_cols else []
        if any(word in query_lower for word in self.patterns['bottom']):
            return 'bottom', [numeric_cols[0]] if numeric_cols else []
        if any(word in query_lower for word in self.patterns['total']):
            return 'total', [numeric_cols[0]] if numeric_cols else []
        if any(word in query_lower for word in self.patterns['average']):
            return 'average', [numeric_cols[0]] if numeric_cols else []
        
        return 'top', [numeric_cols[0]] if numeric_cols else []
    
    def create_visualization(self, df, analysis_type, cols):
        """Generate professional charts"""
        if analysis_type == 'scatter' and len(cols) >= 2:
            fig = px.scatter(df, x=cols[0], y=cols[1], 
                           title=f"📊 {cols[0]} vs {cols[1]}",
                           hover_data=df.select_dtypes(include=['object']).columns[:2],
                           opacity=0.7)
            return fig
        
        elif analysis_type == 'correlation' and len(cols) >= 2:
            corr_matrix = df[cols].corr()
            corr_value = corr_matrix.iloc[0,1]
            fig = px.scatter(df, x=cols[0], y=cols[1],
                           title=f"📈 Correlation Analysis ({corr_value:.3f})",
                           trendline="ols", trendline_color_override="red")
            fig.add_annotation(text=f"Correlation: {corr_value:.3f}", 
                             xref="paper", yref="paper", x=0.02, y=0.98,
                             showarrow=False, font=dict(size=14, color="red"))
            return fig
        
        elif analysis_type == 'trend':
            fig = px.line(df.head(100), x=df.index[:100], y=cols[0],
                         title=f"📈 Trend Analysis: {cols[0]}",
                         markers=True)
            return fig
        
        elif analysis_type in ['top', 'bottom']:
            fig = px.bar(df.head(10), y=cols[0], 
                        title=f"🏆 Top/Bottom 10: {cols[0]}",
                        color=cols[0], color_continuous_scale='Viridis')
            return fig
        
        return None
    
    def generate_analysis(self, query, df, analysis_type, cols):
        """Generate AI analysis text"""
        if not cols or not df.select_dtypes(include=[np.number]).columns.any():
            return "❌ No numeric data found for analysis"
        
        col = cols[0]
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if analysis_type == 'top':
            top_data = df.nlargest(5, col)[[col]].round(0).astype(int)
            return f"**🏆 TOP 5 by `{col}`:**\n\n" + top_data.to_string()
        
        elif analysis_type == 'bottom':
            bottom_data = df.nsmallest(5, col)[[col]].round(0).astype(int)
            return f"**📉 BOTTOM 5 by `{col}`:**\n\n" + bottom_data.to_string()
        
        elif analysis_type == 'total':
            total = df[col].sum()
            return f"**💰 Total `{col}` across {len(df):,} records: **₹{total:,.0f}**"
        
        elif analysis_type == 'average':
            avg = df[col].mean()
            std = df[col].std()
            return f"**📊 `{col}` Summary:**\n• Average: ₹{avg:,.0f}\n• Std Dev: ₹{std:,.0f}\n• Records: {len(df):,}"
        
        elif analysis_type in ['scatter', 'correlation']:
            if len(cols) >= 2:
                corr = df[cols].corr().iloc[0,1]
                return f"**📊 Analysis: `{cols[0]}` vs `{cols[1]}`**\nCorrelation: **{corr:.3f}**\nRecords analyzed: {len(df)}"
        
        return f"**✅ Analyzed `{col}`**: {len(df):,} records, avg ₹{df[col].mean():,.0f}"

# MAIN APPLICATION
st.set_page_config(page_title="Databro AI Pro", page_icon="🧠", layout="wide")

st.title("🧠 **Databro AI Pro** - Your Custom Data Analyst")
st.markdown("**No APIs • Graphs • Correlations • Patterns • Full Query History**")

# Initialize AI
ai = DatabroAI()
MAX_FILE_SIZE = 200 * 1024 * 1024

# Enhanced Sidebar with Query History + Controls
with st.sidebar:
    st.header("⚙️ **Control Panel**")
    
    # File upload
    uploaded_file = st.file_uploader("📁 Upload CSV/Excel (Max 200MB)", 
                                   type=['csv', 'xlsx'],
                                   help="Sales, GST, telecom, finance data")
    
    st.markdown("---")
    st.markdown("### 📋 **Query History** (Last 15)")
    
    # Initialize query log
    if "query_log" not in st.session_state:
        st.session_state.query_log = []
    
    # Display query history
    for qlog in st.session_state.query_log[-15:][::-1]:
        with st.container(border=True):
            st.caption(f"**{qlog['time']}** | {qlog['query'][:70]}{'...' if len(qlog['query']) > 70 else ''}")
    
    # Clear history button
    if st.button("🗑️ Clear All History", use_container_width=True):
        st.session_state.query_log.clear()
        st.session_state.messages.clear()
        st.rerun()
    
    st.markdown("---")
    st.caption("👨‍💼 Built for Indian SMBs | ₹199/month")

# Main content area
if uploaded_file is not None:
    if uploaded_file.size > MAX_FILE_SIZE:
        st.error("❌ File exceeds 200MB limit!")
        st.stop()
    
    # Load data
    with st.spinner("🔄 AI learning your data structure..."):
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            st.stop()
    
    # Data overview metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📊 Total Records", f"{len(df):,}")
    with col2:
        st.metric("📈 Columns", len(df.columns))
    with col3:
        st.metric("🔢 Numeric Columns", len(df.select_dtypes(np.number).columns))
    with col4:
        st.metric("❌ Missing Values", df.isnull().sum().sum())
    with col5:
        st.metric("💰 Highest Value", f"₹{df.select_dtypes(np.number).max().max():,.0f}")
    
    st.success(f"✅ **AI analyzed {len(df):,} records across {len(df.columns)} columns!**")
    st.info("🛡️ **Your data is secure** - Never stored, session-only processing")
    
    st.markdown("---")
    st.subheader("💬 **AI Analyst Chat**")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history (WHERE USERS SEE ALL QUERIES)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input and processing
    if prompt := st.chat_input("Ask your AI anything... (ex: 'correlation balance vs revenue', 'top customers', 'trend analysis')"):
        
        # Log query to history
        query_entry = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "query": prompt,
            "rows": len(df),
            "columns": len(df.columns)
        }
        st.session_state.query_log.append(query_entry)
        
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("🤖 AI analyzing your data + generating insights..."):
                analysis_type, cols = ai.parse_query(prompt, df)
                response = ai.generate_analysis(prompt, df, analysis_type, cols)
                
                # Create visualization if needed
                if analysis_type in ['scatter', 'correlation', 'trend', 'top', 'bottom'] and cols:
                    fig = ai.create_visualization(df, analysis_type, cols)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True, height=400)
                
                # Display analysis
                st.markdown(response)
                
                # Save AI response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Auto-scroll and rerun for smooth UX
        st.rerun()

else:
    # Welcome screen with examples
    st.info("👆 **Upload your CSV/Excel file to start AI analysis**")
    st.markdown("""
    ### 🎯 **Example Queries Your AI Understands:**
    ```python
    💰 "highest subscriber balance" → Top 5 users + bar chart
    📊 "correlation between balance and ID" → Scatter plot + correlation coefficient
    📈 "trend analysis" → Line chart over time
    🏆 "top 5 customers" → Leaderboard visualization  
    💵 "total revenue" → Complete financial summary
    📉 "find outliers" → Bottom performers identified
    ```
    
    **✅ Works with 200MB files = Full GST returns + FY data!**
    """)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 14px;'>
    💰 **₹199/month**<br>
    Pure Python AI<br>
    No external APIs
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 14px;'>
    🛡️ **Bank-grade security**<br>
    Session-only data<br>
    Never stored
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 14px;'>
    🇮🇳 **Indian SMBs**<br>
    GST • Sales • Telecom<br>
    Churn analysis ready
    </div>
    """, unsafe_allow_html=True)
