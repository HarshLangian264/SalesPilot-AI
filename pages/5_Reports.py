"""
5_Reports.py

Final Report page for generating executive analytics reports
and exporting downloadable PDF documents.
"""

import streamlit as st
import pandas as pd

from src.report import (
    get_dataset_overview,
    calculate_data_quality,
    calculate_numeric_statistics,
    calculate_categorical_insights,
    calculate_correlation_insights,
    get_forecast_context,
    build_report_context,
    generate_ai_report,
    create_pdf
)

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Executive Report | SalesPilot AI",
    page_icon="📑",
    layout="wide"
)

st.title("📑 Executive Business Analytics Report")
st.caption(
    "Generate comprehensive, human-friendly business reports powered by "
    "deterministic Python analytics and AI synthesis."
)

# ==========================================================
# 1. CHECK DATASET
# ==========================================================

if "clean_df" not in st.session_state:
    st.warning("No dataset is available. Please upload a dataset on the Upload Data page first.")
    st.stop()

df = st.session_state["clean_df"]

if df is None or df.empty:
    st.warning("The currently uploaded dataset is empty.")
    st.stop()

# ==========================================================
# 2. CALCULATE DETERMINISTIC FACTS (Top-to-Bottom Flow)
# ==========================================================

overview = get_dataset_overview(df)
data_quality = calculate_data_quality(df)
numeric_statistics = calculate_numeric_statistics(df)
categorical_insights = calculate_categorical_insights(df)
correlation_insights = calculate_correlation_insights(df)
forecast_context = get_forecast_context(st.session_state)

report_context = build_report_context(
    overview=overview,
    data_quality=data_quality,
    numeric_statistics=numeric_statistics,
    categorical_insights=categorical_insights,
    correlation_insights=correlation_insights,
    forecast_context=forecast_context
)

# ==========================================================
# 3. ANALYSIS PREVIEW
# ==========================================================

st.subheader("🔍 Calculated Analysis Preview")
st.caption("Review the calculated facts below before asking Gemini to synthesize the final report.")

tab_overview, tab_numeric, tab_categorical, tab_correlations, tab_forecast = st.tabs([
    "📊 Dataset Overview & Quality",
    "📈 Numerical Statistics",
    "🏷️ Categorical Insights",
    "🔗 Correlations",
    "🔮 Forecast Outlook"
])

with tab_overview:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Rows", f"{overview['rows']:,}")
    with col2:
        st.metric("Total Columns", overview['columns'])
    with col3:
        st.metric("Completeness Rate", f"{data_quality['completeness_pct']}%")
    with col4:
        st.metric("Duplicate Rows", data_quality['duplicate_rows'])

    st.write("**Columns Overview:**", ", ".join(overview['column_names']))
    if data_quality['missing_by_column']:
        st.warning(f"Missing Values detected: {data_quality['missing_by_column']}")
    else:
        st.success("No missing values found across all columns.")

with tab_numeric:
    if numeric_statistics:
        num_df = pd.DataFrame(numeric_statistics).T
        st.dataframe(num_df, use_container_width=True)
    else:
        st.info("No numerical columns found in the dataset.")

with tab_categorical:
    if categorical_insights:
        for cat_col, cat_data in categorical_insights.items():
            with st.expander(f"Category: {cat_col} ({cat_data['unique_count']} unique values)"):
                st.write(f"**Dominant Category:** {cat_data['dominant_category']}")
                st.write("**Top Categories Count:**", cat_data['top_categories_count'])
    else:
        st.info("No suitable categorical columns found for grouping.")

with tab_correlations:
    if "correlation_matrix" in correlation_insights and correlation_insights["correlation_matrix"]:
        corr_matrix_df = pd.DataFrame(correlation_insights["correlation_matrix"])
        st.dataframe(corr_matrix_df, use_container_width=True)
        if correlation_insights.get("strongest_positive"):
            st.write("**Strongest Positive Correlations:**", correlation_insights["strongest_positive"])
    else:
        st.info("Insufficient numerical columns for correlation analysis.")

with tab_forecast:
    if forecast_context.get("available"):
        st.success(f"Forecast available ({forecast_context['total_periods']} periods).")
        st.dataframe(pd.DataFrame(forecast_context["forecast_summary"]), use_container_width=True)
    else:
        st.info("No forecast model has been run yet. You can generate a forecast on the Forecasting page.")

st.divider()

# ==========================================================
# 4. GENERATE AI REPORT
# ==========================================================

st.subheader("🤖 AI Report Generation")

col_gen, col_clear = st.columns([3, 1])

with col_gen:
    if st.button("🚀 Generate AI Business Report", type="primary", use_container_width=True):
        try:
            with st.spinner("Synthesizing verified analysis into an executive report..."):
                ai_report_text = generate_ai_report(report_context)
                st.session_state["ai_report_text"] = ai_report_text
            st.success("Executive report generated successfully!")
        except Exception as e:
            st.error(f"Failed to generate report: {e}")

with col_clear:
    if "ai_report_text" in st.session_state:
        if st.button("🗑️ Clear Report", use_container_width=True):
            st.session_state.pop("ai_report_text", None)
            st.rerun()

# ==========================================================
# 5. DISPLAY REPORT & DOWNLOAD PDF
# ==========================================================

if "ai_report_text" in st.session_state:
    st.divider()
    st.subheader("📑 Generated Business Report")
    
    st.markdown(st.session_state["ai_report_text"])

    st.divider()

    # Generate PDF Byte Stream
    try:
        pdf_bytes = create_pdf(
            report_text=st.session_state["ai_report_text"],
            metadata={"rows": overview["rows"], "columns": overview["columns"]}
        )

        st.download_button(
            label="📥 Download Report as PDF",
            data=pdf_bytes,
            file_name="Executive_Sales_Analytics_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Failed to generate PDF document: {e}")
