import streamlit as st
import pandas as pd

try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    from snowflake.snowpark import Session
    session = Session.builder.config('connection_name', 'default').create()

st.title("Query Token Consumption Analyzer")

@st.cache_data(ttl=300)
def get_queries_with_tokens(_session):
    query = """
    SELECT 
        qh.QUERY_ID,
        qh.QUERY_TEXT,
        qh.USER_NAME,
        qh.START_TIME,
        qh.TOTAL_ELAPSED_TIME,
        qh.EXECUTION_STATUS,
        cu.MODEL_NAME,
        cu.FUNCTION_NAME,
        cu.TOKENS,
        cu.TOKEN_CREDITS,
        cu.TOKENS_GRANULAR,
        cu.TOKEN_CREDITS_GRANULAR
    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY qh
    INNER JOIN SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AISQL_USAGE_HISTORY cu
        ON qh.QUERY_ID = cu.QUERY_ID
    WHERE qh.START_TIME >= DATEADD(day, -30, CURRENT_TIMESTAMP())
    ORDER BY qh.START_TIME DESC
    LIMIT 1000
    """
    return _session.sql(query).to_pandas()

with st.spinner("Loading queries with token usage..."):
    try:
        df = get_queries_with_tokens(session)
        
        if df.empty:
            st.warning("No queries with token usage found in the last 30 days.")
            st.stop()
        
        st.sidebar.header("Filters")
        
        users = ["All"] + sorted(df["USER_NAME"].dropna().unique().tolist())
        selected_user = st.sidebar.selectbox("User", users)
        
        models = ["All"] + sorted(df["MODEL_NAME"].dropna().unique().tolist())
        selected_model = st.sidebar.selectbox("Model", models)
        
        functions = ["All"] + sorted(df["FUNCTION_NAME"].dropna().unique().tolist())
        selected_function = st.sidebar.selectbox("Function", functions)
        
        filtered_df = df.copy()
        if selected_user != "All":
            filtered_df = filtered_df[filtered_df["USER_NAME"] == selected_user]
        if selected_model != "All":
            filtered_df = filtered_df[filtered_df["MODEL_NAME"] == selected_model]
        if selected_function != "All":
            filtered_df = filtered_df[filtered_df["FUNCTION_NAME"] == selected_function]
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Queries", len(filtered_df))
        col2.metric("Total Tokens", f"{filtered_df['TOKENS'].sum():,.0f}")
        col3.metric("Total Credits", f"{filtered_df['TOKEN_CREDITS'].sum():.4f}")
        col4.metric("Avg Tokens/Query", f"{filtered_df['TOKENS'].mean():,.0f}")
        
        st.subheader("Select a query to view details")
        
        display_df = filtered_df[["QUERY_ID", "START_TIME", "USER_NAME", "MODEL_NAME", "FUNCTION_NAME", "TOKENS", "TOKEN_CREDITS"]].copy()
        display_df["QUERY_PREVIEW"] = filtered_df["QUERY_TEXT"].str[:100] + "..."
        
        selection = st.dataframe(
            display_df,
            column_config={
                "QUERY_ID": "Query ID",
                "START_TIME": st.column_config.DatetimeColumn("Start Time", format="YYYY-MM-DD HH:mm:ss"),
                "USER_NAME": "User",
                "MODEL_NAME": "Model",
                "FUNCTION_NAME": "Function",
                "TOKENS": st.column_config.NumberColumn("Tokens", format="%d"),
                "TOKEN_CREDITS": st.column_config.NumberColumn("Credits", format="%.6f"),
                "QUERY_PREVIEW": "Query Preview"
            },
            hide_index=True,
            use_container_width=True,
            selection_mode="single-row",
            on_select="rerun"
        )
        
        if selection and selection.selection.rows:
            selected_idx = selection.selection.rows[0]
            selected_row = filtered_df.iloc[selected_idx]
            
            st.divider()
            st.subheader("Query Details")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Query ID:** `{selected_row['QUERY_ID']}`")
                st.markdown(f"**User:** {selected_row['USER_NAME']}")
                st.markdown(f"**Model:** {selected_row['MODEL_NAME']}")
                st.markdown(f"**Function:** {selected_row['FUNCTION_NAME']}")
            with col2:
                st.markdown(f"**Start Time:** {selected_row['START_TIME']}")
                st.markdown(f"**Elapsed Time:** {selected_row['TOTAL_ELAPSED_TIME']} ms")
                st.markdown(f"**Status:** {selected_row['EXECUTION_STATUS']}")
            
            st.subheader("Token Consumption")
            tok_col1, tok_col2 = st.columns(2)
            with tok_col1:
                st.metric("Total Tokens", f"{selected_row['TOKENS']:,}")
            with tok_col2:
                st.metric("Token Credits", f"{selected_row['TOKEN_CREDITS']:.6f}")
            
            if selected_row['TOKENS_GRANULAR']:
                st.markdown("**Token Breakdown:**")
                st.json(selected_row['TOKENS_GRANULAR'])
            
            if selected_row['TOKEN_CREDITS_GRANULAR']:
                st.markdown("**Credit Breakdown:**")
                st.json(selected_row['TOKEN_CREDITS_GRANULAR'])
            
            st.subheader("Full Query Text")
            st.code(selected_row['QUERY_TEXT'], language="sql")
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Make sure you have access to SNOWFLAKE.ACCOUNT_USAGE views. You may need the ACCOUNTADMIN role or appropriate privileges.")
