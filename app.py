import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

from src.csv_handler import load_and_clean_csv
from src.database import create_connection, load_df_to_sqlite, execute_query
from src.schema import get_schema
from src.sql_generator import generate_sql
from src.sql_validator import validate_sql_safety
from src.visualizer import generate_visualization
from src.insights import generate_insights

load_dotenv()

def init_session_state():
    if "df" not in st.session_state:
        st.session_state.df = None
    if "db_conn" not in st.session_state:
        st.session_state.db_conn = None
    if "schema" not in st.session_state:
        st.session_state.schema = None
    if "table_name" not in st.session_state:
        st.session_state.table_name = "data_table"

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def main():
    st.set_page_config(page_title="LangChain SQL Data Analyst", layout="wide", page_icon="📊")
    
    st.markdown("""
        <style>
        .stApp {
            background-color: #f8f9fa;
        }
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1E3A8A;
            margin-bottom: 0px;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #4B5563;
            margin-bottom: 2rem;
        }
        .insight-box {
            background-color: #E0F2FE;
            border-left: 5px solid #0284C7;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 2rem;
            color: #0369A1;
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)
    
    init_session_state()
    
    with st.sidebar:
        st.title("📊 Data Analyst")
        st.markdown("Upload a CSV file and ask questions about your data in natural language.")
        
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
        
        if st.button("Clear Data / New Dataset", use_container_width=True):
            st.session_state.df = None
            st.session_state.db_conn = None
            st.session_state.schema = None
            st.rerun()
            
        if uploaded_file is not None and st.session_state.df is None:
            try:
                with st.spinner("Reading dataset..."):
                    df = load_and_clean_csv(uploaded_file)
                    st.session_state.df = df
                    
                with st.spinner("Creating database..."):
                    conn = create_connection()
                    load_df_to_sqlite(df, st.session_state.table_name, conn)
                    st.session_state.db_conn = conn
                    
                with st.spinner("Understanding schema..."):
                    schema = get_schema(conn, st.session_state.table_name)
                    st.session_state.schema = schema
                    
            except Exception as e:
                st.error(f"Error processing file: {e}")
                
        if st.session_state.df is not None:
            st.success("Dataset loaded successfully!")
            st.subheader("File Information")
            st.write(f"**Rows:** {st.session_state.df.shape[0]:,}")
            st.write(f"**Columns:** {st.session_state.df.shape[1]}")
            
            with st.expander("View Columns"):
                for col in st.session_state.df.columns:
                    st.write(f"- `{col}`")

    st.markdown('<p class="main-header">LangChain SQL Data Analyst</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Ask natural language questions about your uploaded CSV data powered by Open Source LLMs.</p>', unsafe_allow_html=True)
    
    if st.session_state.df is None:
        st.info("👈 Please upload a CSV file in the sidebar to get started.")
        return
        
    question = st.text_input("Ask a question about your data:", placeholder="e.g., Which 5 products generated the highest revenue?")
    
    if st.button("Ask Data", type="primary"):
        if not question:
            st.warning("Please enter a question.")
            return
            
        try:
            with st.spinner("Generating SQL..."):
                sql_query = generate_sql(question, st.session_state.schema)
                
            with st.spinner("Validating SQL safety..."):
                validate_sql_safety(sql_query)
                
            with st.spinner("Running query..."):
                result_df = execute_query(sql_query, st.session_state.db_conn)
                
            with st.spinner("Generating insights..."):
                insight = generate_insights(result_df, question)
                
            st.markdown("---")
            
            st.markdown(f'<div class="insight-box">💡 <b>Insight:</b> {insight}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Query Results")
                st.dataframe(result_df, use_container_width=True, hide_index=True)
                
                if not result_df.empty:
                    csv_data = convert_df_to_csv(result_df)
                    st.download_button(
                        label="Download Results as CSV",
                        data=csv_data,
                        file_name='query_results.csv',
                        mime='text/csv',
                    )
                    
            with col2:
                st.subheader("Visualization")
                with st.spinner("Creating visualization..."):
                    generate_visualization(result_df)
                    
            with st.expander("View Generated SQL Query"):
                st.code(sql_query, language="sql")
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
