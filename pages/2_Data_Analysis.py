import streamlit as st
import importlib
import src.config
importlib.reload(src.config)
import src.visualization
importlib.reload(src.visualization)
from src.visualization import datavisualizer


st.set_page_config(
    page_title="Data Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data Analysis Dashboard")

# --------------------------------------------------
# Check if dataset exists
# --------------------------------------------------

if "clean_df" not in st.session_state:

    st.warning("⚠️ Please upload and preprocess a dataset first.")

    st.stop()

df = st.session_state["clean_df"]

visualizer = datavisualizer(df)

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

st.header("📌 Key Performance Indicators")

kpis = visualizer.get_kpis()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${kpis['total_sales']:,.2f}")
col2.metric("Total Profit", f"${kpis['total_profit']:,.2f}")
col3.metric("Total Orders", kpis["total_orders"])

col4, col5, col6 = st.columns(3)

col4.metric("Average Sales", f"${kpis['average_sales']:,.2f}")
col5.metric("Total Quantity", kpis["total_quantity"])
col6.metric("Average Profit", f"${kpis['average_profit']:,.2f}")

st.divider()

# --------------------------------------------------
# SALES TRENDS
# --------------------------------------------------

st.header("📈 Sales Trends")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        visualizer.plot_sales_trend(),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        visualizer.plot_monthly_sales(),
        use_container_width=True
    )

st.plotly_chart(
    visualizer.plot_sales_by_year(),
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

st.header("📊 Business Insights")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        visualizer.plot_sales_by_category(),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        visualizer.plot_sales_by_region(),
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# PRODUCT ANALYSIS
# --------------------------------------------------

st.header("📦 Product Analysis")

st.plotly_chart(
    visualizer.plot_top_products(),
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# PROFIT ANALYSIS
# --------------------------------------------------

st.header("💰 Profit Analysis")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        visualizer.plot_profit_distribution(),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        visualizer.plot_correlation_heatmap(),
        use_container_width=True
    )