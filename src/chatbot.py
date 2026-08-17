from src.intent import IntentDetector
from src.ai_response import AIResponseGenerator
from src.forecast import ForecastEngine


class ChatBot:

    def __init__(self, dataframe, max_cardinality: int = 50):
        """
        Initialize the chatbot.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            Cleaned dataset.
        max_cardinality : int
            Threshold for categorical columns. Columns with unique values
            exceeding this limit will be ignored as high-cardinality/IDs.
        """

        self.df = dataframe
        self.max_cardinality = max_cardinality

        self.intent_detector = IntentDetector()
        self.ai = AIResponseGenerator()
        self.forecast_engine = ForecastEngine()

    # ==================================================
    # DATASET SUMMARY
    # ==================================================

    def _dataset_summary(self):
        """
        Create a basic summary of the dataset.
        """

        if self.df is None or self.df.empty:
            return "No dataset is currently available."

        columns_info = []
        for col in self.df.columns:
            dtype = str(self.df[col].dtype)
            non_null = self.df[col].count()
            columns_info.append(f" - {col} ({dtype}): {non_null} non-null values")

        summary = f"""
Dataset Shape: {len(self.df)} rows, {len(self.df.columns)} columns

Columns Overview:
{chr(10).join(columns_info)}
"""

        return summary.strip()

    # ==================================================
    # ANALYSIS CONTEXT
    # ==================================================

    def _analysis_context(self):
        """
        Create generic analysis information.

        Dynamically inspects DataFrame numerical and categorical columns
        without assuming specific column names.
        """

        if self.df is None or self.df.empty:
            return {
                "dataset_summary": "No dataset available.",
                "analysis_result": "No analysis could be performed because no dataset is loaded."
            }

        numeric_columns = (
            self.df
            .select_dtypes(include="number")
            .columns
            .tolist()
        )

        categorical_columns = (
            self.df
            .select_dtypes(
                include=["object", "category", "string"]
            )
            .columns
            .tolist()
        )

        analysis_parts = []

        # ----------------------------------------------
        # Numerical statistics
        # ----------------------------------------------

        if numeric_columns:

            numeric_summary = (
                self.df[numeric_columns]
                .describe()
                .round(2)
                .to_string()
            )

            analysis_parts.append(
                "Overall Numerical Statistics:\n"
                + numeric_summary
            )

        # ----------------------------------------------
        # Categorical vs numerical analysis
        # ----------------------------------------------

        for category_column in categorical_columns:

            unique_count = (
                self.df[category_column]
                .nunique(dropna=True)
            )

            # Ignore high-cardinality columns (such as IDs, Customer Names, Order IDs)
            if unique_count == 0 or unique_count > self.max_cardinality or unique_count == len(self.df):
                continue

            for numeric_column in numeric_columns:

                grouped = (
                    self.df
                    .groupby(category_column, observed=False)[numeric_column]
                    .agg(["sum", "mean", "count"])
                    .sort_values(by="sum", ascending=False)
                    .head(10)
                    .round(2)
                )

                if not grouped.empty:

                    analysis_parts.append(
                        f"Top Performers ({numeric_column} grouped by {category_column}):\n"
                        f"{grouped.to_string()}"
                    )

        # ----------------------------------------------
        # Correlation
        # ----------------------------------------------

        if len(numeric_columns) >= 2:

            correlation = (
                self.df[numeric_columns]
                .corr()
                .round(2)
            )

            analysis_parts.append(
                "Correlation Matrix:\n"
                + correlation.to_string()
            )

        # ----------------------------------------------
        # Final analysis result
        # ----------------------------------------------

        if analysis_parts:

            analysis_result = "\n\n".join(
                analysis_parts
            )

        else:

            analysis_result = (
                "No suitable numerical or categorical "
                "relationships were found in the current dataset."
            )

        return {
            "dataset_summary": self._dataset_summary(),
            "analysis_result": analysis_result
        }

    # ==================================================
    # FORECAST CONTEXT
    # ==================================================

    def _forecast_context(self, result):
        """
        Generate forecast context using the entities
        extracted by IntentDetector.
        """

        if self.df is None or self.df.empty:

            return {
                "dataset_summary": "No dataset available.",
                "forecast_result": (
                    "Forecast cannot be generated because no dataset is loaded."
                )
            }

        # ----------------------------------------------
        # Get forecast entities
        # ----------------------------------------------

        entities = result.get("entities", {})

        periods = entities.get("periods", 12)

        frequency = entities.get("frequency", "M")

        # ----------------------------------------------
        # Prepare historical data & Train & Forecast
        # ----------------------------------------------

        try:
            self.forecast_engine.prepare_time_series(
                self.df
            )

            self.forecast_engine.train_forecasting_model()

            forecast = self.forecast_engine.forecast(
                periods=periods,
                frequency=frequency
            )

            if hasattr(forecast, "to_string"):
                forecast_result = forecast.to_string(index=False)
            else:
                forecast_result = str(forecast)

        except Exception as e:
            forecast_result = (
                f"Could not generate forecast: {str(e)}. "
                "Please verify that your dataset contains valid date and target columns."
            )

        return {
            "dataset_summary": self._dataset_summary(),
            "forecast_result": forecast_result
        }

    # ==================================================
    # GENERAL CONTEXT
    # ==================================================

    def _general_context(self):
        """
        Create context for general questions.
        """

        return {
            "dataset_summary": self._dataset_summary()
        }

    # ==================================================
    # MAIN CHAT FUNCTION
    # ==================================================

    def chat(self, question):
        """
        Process a user's question.

        Parameters
        ----------
        question : str
            User's natural-language question.

        Returns
        -------
        str
            AI-generated response.
        """

        if not question or not question.strip():

            return "Please enter a question."

        # ----------------------------------------------
        # Handle Missing Dataset
        # ----------------------------------------------

        if self.df is None or self.df.empty:

            result = self.intent_detector.detect(question)
            intent = result.get("intent", "general_chat")

            if intent in ["analysis", "forecast", "business_advice", "visualization", "summary"]:
                intent = "no_dataset"
                context = {}
            else:
                intent = "general_chat"
                context = {"dataset_summary": "No dataset is currently uploaded."}

            return self.ai.generate_response(
                intent=intent,
                question=question,
                context=context
            )

        # ----------------------------------------------
        # Detect intent
        # ----------------------------------------------

        result = self.intent_detector.detect(
            question
        )

        intent = result.get(
            "intent",
            "general_chat"
        )

        # ----------------------------------------------
        # Build appropriate context
        # ----------------------------------------------

        if intent == "forecast":

            context = self._forecast_context(
                result
            )

        elif intent in [
            "analysis",
            "business_advice",
            "visualization",
            "summary"
        ]:

            context = self._analysis_context()

        elif intent == "no_dataset":

            context = {}

        else:

            context = self._general_context()
            intent = "general_chat"

        # ----------------------------------------------
        # Generate Gemini response
        # ----------------------------------------------

        try:
            response = self.ai.generate_response(
                intent=intent,
                question=question,
                context=context
            )
            return response
        except Exception as e:
            return f"An error occurred while generating the AI response: {str(e)}"