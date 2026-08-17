
import os
import joblib
import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (mean_absolute_error, mean_squared_error, r2_score)
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from src.config import TARGET_COLUMN
class ModelTrainer:

    def __init__(self, df):

        # initialize the model trainer with cleaned dataset 
        
        self.df = df
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

        self.models = {}
        self.results = {}

    def prepare_training_data(self):
        # prepare the dataset for machine learning.

        if self.df is None:
            raise ValueError("Dataset is empty.")

        df_copy = self.df.copy()
        
        if TARGET_COLUMN not in df_copy.columns:
            raise ValueError(f"Target column '{TARGET_COLUMN}' not found in dataset.")

        X = df_copy.drop(columns=[TARGET_COLUMN])
        y = df_copy[TARGET_COLUMN]

        # 1. Drop raw datetime columns (ML algorithms require numeric features)
        datetime_cols = X.select_dtypes(include=['datetime64', 'datetime', 'datetimetz']).columns.tolist()
        for col in datetime_cols:
            if f"{col}_year" not in X.columns and "Year" not in X.columns:
                X[f"{col}_year"] = X[col].dt.year
                X[f"{col}_month"] = X[col].dt.month
                X[f"{col}_day"] = X[col].dt.day
            X.drop(columns=[col], inplace=True)

        # 2. Encode categorical and string columns
        label_encoders = {}
        cat_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
        for column in cat_cols:
            encoder = LabelEncoder()
            X[column] = encoder.fit_transform(X[column].astype(str))
            label_encoders[column] = encoder

        # 3. Ensure all feature columns are strictly numeric
        X = X.apply(pd.to_numeric, errors='coerce').fillna(0)

        self.label_encoders = label_encoders
        self.X = X
        self.y = y
        (self.X_train, self.X_test, self.y_train, self.y_test) = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

 
    def train_linear_regression(self):
        #Train a Linear Regression model and evaluate its performance.

        if self.X_train is None:
            raise ValueError("Training data not prepared. Call prepare_training_data() first.")

        # Create model
        model = LinearRegression()

        # Train model
        model.fit(self.X_train, self.y_train)

        # Make predictions
        predictions = model.predict(self.X_test)

        # Evaluate model
        mae = mean_absolute_error(self.y_test, predictions)
        rmse = np.sqrt(mean_squared_error(self.y_test, predictions))
        r2 = r2_score(self.y_test, predictions)

        # Store model
        self.models["Linear Regression"] = model

        # Store results
        self.results["Linear Regression"] = {
            "MAE": round(mae, 2),
            "RMSE": round(rmse, 2),
            "R2 Score": round(r2, 4)
        }

        return self.results["Linear Regression"]

    def train_decision_tree(self):
        # Train a Decision Tree Regressor and evaluate its performance.

        if self.X_train is None:
            raise ValueError("Training data not prepared. Call prepare_training_data() first." )

        # Create model
        model = DecisionTreeRegressor(
            random_state=42,
            max_depth=10
        )

        # Train model
        model.fit(self.X_train, self.y_train)

        # Make predictions
        predictions = model.predict(self.X_test)

        # Evaluate model
        mae = mean_absolute_error(self.y_test, predictions)
        rmse = np.sqrt(mean_squared_error(self.y_test, predictions))
        r2 = r2_score(self.y_test, predictions)

        # Store model
        self.models["Decision Tree"] = model

        # Store results
        self.results["Decision Tree"] = {
            "MAE": round(mae, 2),
            "RMSE": round(rmse, 2),
            "R2 Score": round(r2, 4)
        }

        return self.results["Decision Tree"]
        

    def train_random_forest(self):
    
    # Train a Random Forest Regressor and evaluate its performance.

        if self.X_train is None:
            raise ValueError(
                "Training data not prepared. Call prepare_training_data() first."
            )

        # Create model
        model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            max_depth=15,
            n_jobs=-1
        )

        # Train model
        model.fit(self.X_train, self.y_train)

        # Make predictions
        predictions = model.predict(self.X_test)

        # Evaluate model
        mae = mean_absolute_error(self.y_test, predictions)
        rmse = np.sqrt(mean_squared_error(self.y_test, predictions))
        r2 = r2_score(self.y_test, predictions)

        # Store model
        self.models["Random Forest"] = model

        # Store results
        self.results["Random Forest"] = {
            "MAE": round(mae, 2),
            "RMSE": round(rmse, 2),
            "R2 Score": round(r2, 4)
        }

        return self.results["Random Forest"]
        


    def train_xgboost(self):
        
        #Train an XGBoost Regressor and evaluate its performance.
        if self.X_train is None:
            raise ValueError("Training data not prepared. Call prepare_training_data() first.")

        # Create model
        model = XGBRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42,
            objective="reg:squarederror"
        )

        # Train model
        model.fit(self.X_train, self.y_train)

        # Make predictions
        predictions = model.predict(self.X_test)

        # Evaluate model
        mae = mean_absolute_error(self.y_test, predictions)
        rmse = np.sqrt(mean_squared_error(self.y_test, predictions))
        r2 = r2_score(self.y_test, predictions)

        # Store model
        self.models["XGBoost"] = model

        # Store results
        self.results["XGBoost"] = {
            "MAE": round(mae, 2),
            "RMSE": round(rmse, 2),
            "R2 Score": round(r2, 4)
        }

        return self.results["XGBoost"]

    def compare_models(self , sort_by = "R2 Score"):

    #Compare all trained models based on evaluation metrics.
    

        if not self.results:
            raise ValueError("No models have been trained.")

        comparison_df = pd.DataFrame(self.results).T

        comparison_df = comparison_df.sort_values(
            by="R2 Score",
            ascending=(sort_by != "R2 Score")
        )

        comparison_df.reset_index(inplace=True)

        comparison_df.rename(
            columns={"index": "Model"},
            inplace=True
        )

        return comparison_df

    def save_best_model(self, save_path="models"):
        # Save the best performing model based on R2 Score

        if not self.models:
            raise ValueError("No trained models available.")

        comparison_df = self.compare_models()

        best_model_name = comparison_df.iloc[0]["Model"]

        best_model = self.models[best_model_name]

        os.makedirs(save_path, exist_ok=True)

        model_path = os.path.join(
            save_path,
            "best_model.pkl"
        )

        joblib.dump(best_model, model_path)

        return {
            "model_name": best_model_name,
            "model_path": model_path
        }