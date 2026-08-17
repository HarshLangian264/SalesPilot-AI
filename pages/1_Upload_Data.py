import streamlit as st
import importlib
import src.config
importlib.reload(src.config)
import src.preprocessing
importlib.reload(src.preprocessing)
from src.preprocessing import datapreprocessor


st.set_page_config(
    page_title="Upload Dataset",
    page_icon="📂",
    layout="wide"
)

st.title("📂 Upload Sales Dataset")

st.write(
    "Upload a sales dataset (CSV or Excel) to begin preprocessing and analysis."
)

uploaded_file = st.file_uploader(
    "Choose a dataset",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:

    preprocessor = datapreprocessor()

    try:
        # -----------------------------
        # Load Dataset
        # -----------------------------
        preprocessor.load_data(uploaded_file)

        st.success("✅ Dataset uploaded successfully!")

        # -----------------------------
        # Dataset Information
        # -----------------------------
        info = preprocessor.get_dataset_info()

        st.subheader("📊 Dataset Information")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Rows", info["rows"])

        with col2:
            st.metric("Columns", info["columns"])

        with col3:
            st.metric("Duplicate Rows", info["duplicate_rows"])

        st.subheader("📋 Dataset Preview")

        st.dataframe(
            preprocessor.df.head(),
            use_container_width=True
        )

        # -----------------------------
        # Run Preprocessing
        # -----------------------------
        if st.button("🚀 Run Preprocessing", use_container_width=True):

            cleaned_df = preprocessor.preprocess()

            st.session_state["raw_df"] = preprocessor.df.copy()
            st.session_state["clean_df"] = cleaned_df.copy()
            st.session_state["dataset_info"] = info

            st.success("✅ Preprocessing completed successfully!")

            st.subheader("🧹 Cleaned Dataset")

            st.dataframe(
                cleaned_df.head(),
                use_container_width=True
            )

    except Exception as e:
        st.exception(e)