
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from src.config import DATE_COLUMN, TARGET_COLUMN

class ForecastEngine:

    def __init__(self,model_path = "models/best_model.pkl"):
        self.model_path = Path(model_path)
        self.model = None
        self.history = None
        self.future_dates = None
        self.predictions = None
        self.date_col = DATE_COLUMN
        self.target_col = TARGET_COLUMN
        
        

    def prepare_time_series(self,df):
        if df is None:
            raise ValueError("Dataset is empty")
        if DATE_COLUMN not in df.columns:
            raise ValueError(f"'{DATE_COLUMN}' column not found.")
        if TARGET_COLUMN not in df.columns:
            raise ValueError(f"'{TARGET_COLUMN}' column not found.")    
        # Create a copy
        self.history = df.copy()

        # Convert to datetime
        self.history[DATE_COLUMN] = pd.to_datetime(
            self.history[DATE_COLUMN],
            errors="coerce"
        )

        # Remove invalid dates
        self.history.dropna(
            subset=[DATE_COLUMN],
            inplace=True
        )

        # Sort by date
        self.history.sort_values(
            by=DATE_COLUMN,
            inplace=True
        )

        # Aggregate duplicate dates
        self.history = (
            self.history
            .groupby(DATE_COLUMN, as_index=False)[TARGET_COLUMN]
            .sum()
        )

        # Reset index
        self.history.reset_index(
            drop=True,
            inplace=True
        )

        return self.history        


    def train_forecasting_model(self):
        
        #Train a forecasting model using lag features.

        if self.history is None:
            raise ValueError(
                "Run prepare_time_series() before training."
            )

        target_col = self.target_col

        df = self.history.copy()

        # -----------------------------
        # Create Lag Features
        # -----------------------------

        df["Lag_1"] = df[target_col].shift(1)
        df["Lag_2"] = df[target_col].shift(2)
        df["Lag_3"] = df[target_col].shift(3)

        # Rolling Mean
        df["Rolling_Mean_3"] = (
            df[target_col]
            .rolling(3)
            .mean()
        )

        # Time Features

        date_col = self.date_col

        df["Year"] = df[date_col].dt.year
        df["Month"] = df[date_col].dt.month
        df["Quarter"] = df[date_col].dt.quarter

        # Remove rows containing NaN
        df.dropna(inplace=True)

        feature_columns = [
            "Lag_1",
            "Lag_2",
            "Lag_3",
            "Rolling_Mean_3",
            "Year",
            "Month",
            "Quarter"
        ]

        X = df[feature_columns]

        y = df[target_col]

   

        self.model = RandomForestRegressor(n_estimators=200,random_state=42)

        self.model.fit(X, y)

        self.feature_columns = feature_columns

        return self.model

    def forecast(self,periods=30, frequency="D"):
    

        if self.model is None:
            raise ValueError(
                "Forecast model has not been trained."
            )

        future_df = self.generate_future_dates(
            periods=periods,
            frequency=frequency
        )

        history = self.history.copy()

        target_col = self.target_col

        predictions = []

        for _, row in future_df.iterrows():

            lag_1 = history[target_col].iloc[-1]
            lag_2 = history[target_col].iloc[-2]
            lag_3 = history[target_col].iloc[-3]

            rolling_mean = history[target_col].iloc[-3:].mean()

            features = pd.DataFrame([{
                "Lag_1": lag_1,
                "Lag_2": lag_2,
                "Lag_3": lag_3,
                "Rolling_Mean_3": rolling_mean,
                "Year": row["Year"],
                "Month": row["Month"],
                "Quarter": row["Quarter"]
            }])

            prediction = self.model.predict(features)[0]

            predictions.append(round(prediction, 2))

            new_row = {
                self.date_col: row[self.date_col],
                target_col: prediction
            }

            history = pd.concat(
                [history, pd.DataFrame([new_row])],
                ignore_index=True
            )

        future_df[target_col] = predictions

        return future_df

    def generate_future_dates(self,periods=30, frequency="D"):
        if self.history is None:
            raise ValueError(
            "Prepare the time series before generating future dates."
        )

        freq_alias_map = {"M": "ME", "Q": "QE", "Y": "YE", "A": "YE"}
        norm_freq = freq_alias_map.get(frequency, frequency)

        last_date = self.history[self.date_col].max()

        future_dates = pd.date_range(start=last_date,periods=periods + 1,freq=norm_freq)[1:]

        future_df = pd.DataFrame({
            self.date_col: future_dates
        })

        future_df["Year"] = future_df[self.date_col].dt.year
        future_df["Month"] = future_df[self.date_col].dt.month
        future_df["Quarter"] = future_df[self.date_col].dt.quarter

        self.future_dates = future_df

        return self.future_dates