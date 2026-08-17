import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from src.forecast import ForecastEngine


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Forecast | SalesPilot AI",
    page_icon="📈",
    layout="wide"
)


# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("📈 Forecasting")
st.caption(
    "Generate multi-step forecasts using your trained "
    "machine learning model."
)


# ==========================================================
# CHECK DATASET
# ==========================================================

if "clean_df" not in st.session_state:

    st.warning(
        "No dataset is available. Please upload a dataset first."
    )

    st.stop()


df = st.session_state["clean_df"]


if df is None or df.empty:

    st.warning(
        "The uploaded dataset is empty."
    )

    st.stop()


# ==========================================================
# INITIALIZE FORECAST ENGINE
# ==========================================================

if "forecast_engine" not in st.session_state:

    st.session_state["forecast_engine"] = ForecastEngine()


forecast_engine = st.session_state["forecast_engine"]


# ==========================================================
# FORECAST SETTINGS
# ==========================================================

st.subheader("⚙️ Forecast Settings")

col1, col2 = st.columns(2)


with col1:

    frequency = st.selectbox(
        "Forecast Frequency",
        options=[
            "Daily",
            "Weekly",
            "Monthly",
            "Quarterly",
            "Yearly"
        ],
        index=2
    )


with col2:

    periods = st.number_input(
        "Number of Future Periods",
        min_value=1,
        max_value=365,
        value=6,
        step=1
    )


# Convert UI frequency to pandas frequency

frequency_map = {

    "Daily": "D",

    "Weekly": "W",

    "Monthly": "ME",

    "Quarterly": "QE",

    "Yearly": "YE"
}

pandas_frequency = frequency_map[frequency]


# ==========================================================
# FORECAST BUTTON
# ==========================================================

if st.button(
    "🚀 Generate Forecast",
    type="primary",
    use_container_width=True
):

    try:

        with st.spinner(
            "Preparing data and generating forecast..."
        ):

            # ----------------------------------------------
            # Prepare historical time series
            # ----------------------------------------------

            forecast_engine.prepare_time_series(
                df
            )

            # ----------------------------------------------
            # Train forecasting model
            # ----------------------------------------------

            forecast_engine.train_forecasting_model()

            # ----------------------------------------------
            # Generate forecast
            # ----------------------------------------------

            forecast_result = forecast_engine.forecast(
                periods=int(periods),
                frequency=pandas_frequency
            )

            # Store result in session state

            st.session_state[
                "forecast_result"
            ] = forecast_result

        st.success(
            "Forecast generated successfully!"
        )

    except Exception as e:

        st.error(
            f"Unable to generate forecast: {e}"
        )


# ==========================================================
# DISPLAY FORECAST
# ==========================================================

if "forecast_result" in st.session_state:

    forecast_result = st.session_state[
        "forecast_result"
    ]

    st.divider()

    st.subheader("📊 Forecast Results")


    # ======================================================
    # METRICS
    # ======================================================

    target_column = forecast_engine.target_col

    predictions = forecast_result[
        target_column
    ]


    metric1, metric2, metric3 = st.columns(3)


    with metric1:

        st.metric(
            "Forecast Periods",
            len(forecast_result)
        )


    with metric2:

        st.metric(
            "Average Forecast",
            f"{predictions.mean():,.2f}"
        )


    with metric3:

        st.metric(
            "Highest Forecast",
            f"{predictions.max():,.2f}"
        )


    # ======================================================
    # FORECAST CHART
    # ======================================================

    st.subheader("📈 Forecast Visualization")


    date_column = forecast_engine.date_col


    fig = go.Figure()


    # Historical data

    historical = forecast_engine.history


    fig.add_trace(
        go.Scatter(
            x=historical[date_column],
            y=historical[target_column],
            mode="lines",
            name="Historical"
        )
    )


    # Forecast

    fig.add_trace(
        go.Scatter(
            x=forecast_result[date_column],
            y=forecast_result[target_column],
            mode="lines+markers",
            name="Forecast"
        )
    )


    fig.update_layout(

        title=f"{target_column} Forecast",

        xaxis_title="Date",

        yaxis_title=target_column,

        template="plotly_white",

        hovermode="x unified",

        height=500
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ======================================================
    # FORECAST TABLE
    # ======================================================

    st.subheader("📋 Forecast Data")


    st.dataframe(
        forecast_result,
        use_container_width=True,
        hide_index=True
    )


    # ======================================================
    # DOWNLOAD
    # ======================================================

    csv = forecast_result.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(

        label="⬇️ Download Forecast CSV",

        data=csv,

        file_name="forecast_results.csv",

        mime="text/csv",

        use_container_width=True
    )