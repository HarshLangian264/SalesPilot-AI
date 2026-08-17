import streamlit as st
from src.machine_learning import ModelTrainer

st.set_page_config(
    page_title="Model Training",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Machine Learning Model Training")
st.markdown("Train multiple machine learning models and compare their performance.")

# --------------------------------------------------
# Check Dataset
# --------------------------------------------------

if "clean_df" not in st.session_state:
    st.warning("⚠️ Please upload and preprocess a dataset first.")
    st.stop()

df = st.session_state["clean_df"]

trainer = ModelTrainer(df)

# --------------------------------------------------
# Model Selection
# --------------------------------------------------

st.subheader("📌 Select Models to Train")

col1, col2 = st.columns(2)

with col1:
    linear = st.checkbox("Linear Regression", value=True)
    decision_tree = st.checkbox("Decision Tree", value=True)

with col2:
    random_forest = st.checkbox("Random Forest", value=True)
    xgboost = st.checkbox("XGBoost", value=True)

# --------------------------------------------------
# Train Models
# --------------------------------------------------

if st.button("🚀 Train Selected Models", use_container_width=True):

    try:

        trainer.prepare_training_data()

        status = st.empty()
        progress = st.progress(0)

        total_models = sum([
            linear,
            decision_tree,
            random_forest,
            xgboost
        ])

        completed = 0

        if total_models == 0:
            st.warning("Please select at least one model.")
            st.stop()

        if linear:
            status.info("Training Linear Regression...")
            trainer.train_linear_regression()
            completed += 1
            progress.progress(completed / total_models)

        if decision_tree:
            status.info("Training Decision Tree...")
            trainer.train_decision_tree()
            completed += 1
            progress.progress(completed / total_models)

        if random_forest:
            status.info("Training Random Forest...")
            trainer.train_random_forest()
            completed += 1
            progress.progress(completed / total_models)

        if xgboost:
            status.info("Training XGBoost...")
            trainer.train_xgboost()
            completed += 1
            progress.progress(completed / total_models)

        status.success("✅ Training Completed Successfully!")

        # Save trainer object for Forecast page
        st.session_state["trainer"] = trainer

        # --------------------------------------------------
        # Model Comparison
        # --------------------------------------------------

        comparison = trainer.compare_models()

        st.subheader("📊 Model Performance Comparison")

        st.dataframe(
            comparison,
            use_container_width=True
        )

        # --------------------------------------------------
        # Best Model
        # --------------------------------------------------

        best_model = comparison.iloc[0]

        st.success(
            f"""
              🏆 Best Model : **{best_model['Model']}**

               R² Score : **{best_model['R2 Score']}**

               RMSE : **{best_model['RMSE']}**

               MAE : **{best_model['MAE']}**
            """
        )

        # --------------------------------------------------
        # Save Model
        # --------------------------------------------------

        if st.button("💾 Save Best Model", use_container_width=True):

            info = trainer.save_best_model()

            st.success(
                f"""
                ✅ Best model saved successfully!

                 **Model :** {info['model_name']}

                **Location :** {info['model_path']}
                """
                 )

    except Exception as e:
        st.error(str(e))