import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def generate_visualization(df: pd.DataFrame):
    if df.empty:
        st.info("No data available to visualize.")
        return

    if df.shape == (1, 1):
        val = df.iloc[0, 0]
        if isinstance(val, (int, float)):
            st.metric(label=df.columns[0], value=f"{val:,.2f}" if isinstance(val, float) else val)
            return

    date_cols = df.select_dtypes(include=['datetime64', 'object']).columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns

    real_date_cols = []
    for col in date_cols:
        try:
            pd.to_datetime(df[col], format='mixed')
            real_date_cols.append(col)
        except (ValueError, TypeError):
            pass

    categorical_cols = [c for c in categorical_cols if c not in real_date_cols]

    if len(real_date_cols) == 1 and len(numeric_cols) >= 1:
        x_col = real_date_cols[0]
        y_col = numeric_cols[0]
        
        df_sorted = df.copy()
        df_sorted[x_col] = pd.to_datetime(df_sorted[x_col], format='mixed')
        df_sorted = df_sorted.sort_values(x_col)
        
        fig = px.line(df_sorted, x=x_col, y=y_col, title=f"{y_col} over time")
        st.plotly_chart(fig, use_container_width=True)
        return

    if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
        x_col = categorical_cols[0]
        y_col = numeric_cols[0]
        
        if 3 <= len(df) <= 15:
            df_sorted = df.sort_values(y_col, ascending=True)
            fig = px.bar(df_sorted, x=y_col, y=x_col, orientation='h', title=f"{y_col} by {x_col}")
        else:
            fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
            
        st.plotly_chart(fig, use_container_width=True)
        return

    st.info("Displaying table only (no suitable simple chart format detected).")
