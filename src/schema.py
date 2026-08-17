
import pandas as pd
from pandas.api.types import (is_numeric_dtype,is_datetime64_any_dtype)


class SchemaDetector:

    def __init__(self, df: pd.DataFrame):

        if df is None or df.empty:
            raise ValueError("Dataset is empty.")

        self.df = df.copy()

        self.schema = {}

    # -------------------------------------------------
    # Date Detection
    # -------------------------------------------------

    def detect_date_column(self):

        # Already datetime
        for col in self.df.columns:
            if is_datetime64_any_dtype(self.df[col]):
                return col

        # Look for columns with date/time keywords in name
        for col in self.df.columns:
            if any(k in col.lower() for k in ["date", "time", "year", "timestamp"]):
                try:
                    converted = pd.to_datetime(self.df[col], errors="coerce")
                    if converted.notna().mean() > 0.5:
                        return col
                except Exception:
                    pass

        # Try converting string/object columns
        for col in self.df.columns:
            if self.df[col].dtype == "object":
                try:
                    converted = pd.to_datetime(
                        self.df[col],
                        errors="coerce"
                    )
                    if converted.notna().mean() > 0.8:
                        return col
                except Exception:
                    pass

        return None

    # -------------------------------------------------
    # Target Detection
    # -------------------------------------------------

    def detect_target_column(self):

        numeric_cols = []
        for col in self.df.columns:
            if is_numeric_dtype(self.df[col]):
                numeric_cols.append(col)

        if not numeric_cols:
            return None

        # Exclude ID, code, postal/zip, index columns from being chosen as target
        candidates = [
            col for col in numeric_cols
            if not any(k in col.lower() for k in ["id", "code", "zip", "postal", "year", "month", "day", "index"])
        ]
        if not candidates:
            candidates = numeric_cols

        # Prioritize target/sales/revenue/amount/total names
        for col in candidates:
            if any(k in col.lower() for k in ["sales", "target", "revenue", "total_amount", "amount"]):
                return col

        # Fallback to highest variance among valid candidates
        variances = self.df[candidates].var()
        return variances.idxmax()

    # -------------------------------------------------
    # Numerical Columns
    # -------------------------------------------------

    def detect_numeric_columns(self):

        numeric = []

        for col in self.df.columns:

            if is_numeric_dtype(self.df[col]):
                numeric.append(col)

        return numeric

    # -------------------------------------------------
    # Categorical Columns
    # -------------------------------------------------

    def detect_categorical_columns(self):

        categorical = []

        for col in self.df.columns:

            if self.df[col].dtype == "object":

                categorical.append(col)

        return categorical

    # -------------------------------------------------
    # Datetime Columns
    # -------------------------------------------------

    def detect_datetime_columns(self):

        datetime_columns = []

        for col in self.df.columns:

            if is_datetime64_any_dtype(self.df[col]):
                datetime_columns.append(col)

        return datetime_columns

    # -------------------------------------------------
    # Build Complete Schema
    # -------------------------------------------------

    def build_schema(self):

        self.schema = {

            "date": self.detect_date_column(),

            "target": self.detect_target_column(),

            "numeric": self.detect_numeric_columns(),

            "categorical": self.detect_categorical_columns(),

            "datetime": self.detect_datetime_columns(),

            "columns": list(self.df.columns)

        }

        return self.schema

    # -------------------------------------------------
    # Get Schema
    # -------------------------------------------------

    def get_schema(self):

        if not self.schema:
            return self.build_schema()

        return self.schema

    # -------------------------------------------------
    # Print Schema
    # -------------------------------------------------

    def display_schema(self):

        schema = self.get_schema()

        print("\nDetected Schema")

        for key, value in schema.items():

            print(f"{key:15}: {value}")

    def save_dataset_config(self, file_path="src/dataset_config.py"):
    
    # Save detected dataset schema.

        schema = self.build_schema()

        with open(file_path, "w") as f:

            f.write('"""\n')
            f.write("Automatically generated.\n")
            f.write('"""\n\n')

            f.write(f'DATE_COLUMN = {repr(schema["date"])}\n')
            f.write(f'TARGET_COLUMN = {repr(schema["target"])}\n')

            numeric = schema["numeric"]
            categorical = schema["categorical"]

            # Optional mappings
            f.write(
                f'CATEGORY_COLUMN = {repr(categorical[0]) if len(categorical) > 0 else None}\n'
            )

            f.write(
                f'REGION_COLUMN = {repr(categorical[1]) if len(categorical) > 1 else None}\n'
            )

            f.write(
                f'PRODUCT_COLUMN = {repr(categorical[2]) if len(categorical) > 2 else None}\n'
            )

            f.write(
                f'PROFIT_COLUMN = {repr(numeric[1]) if len(numeric) > 1 else None}\n'
            )

            f.write(
                f'QUANTITY_COLUMN = {repr(numeric[2]) if len(numeric) > 2 else None}\n'
            )