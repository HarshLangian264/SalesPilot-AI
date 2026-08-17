import io
from pathlib import Path    
import numpy as np
import pandas as pd
from src.config import REQUIRED_COLUMNS,DATE_COLUMN,TARGET_COLUMN,CATEGORY_COLUMN,PROFIT_COLUMN,QUANTITY_COLUMN,REGION_COLUMN,PRODUCT_COLUMN
from src.schema import SchemaDetector
class datapreprocessor:
    def __init__(self):
        self.df = None

    def _get_date_col(self):
        if self.df is None:
            return DATE_COLUMN
        if DATE_COLUMN in self.df.columns:
            return DATE_COLUMN
        for col in ["Date", "Order Date", "order_date", "date", "Ship Date", "Order_Date"]:
            if col in self.df.columns:
                return col
        return DATE_COLUMN

    def _ensure_date_column(self):
        if self.df is not None:
            self.df.columns = [str(col).strip() for col in self.df.columns]
            
            # Map date column
            target_col = DATE_COLUMN if DATE_COLUMN == "Date" else "Date"
            if target_col not in self.df.columns and "Date" not in self.df.columns:
                for candidate in ["Order Date", "order_date", "date", "Ship Date", "Order_Date"]:
                    if candidate in self.df.columns:
                        self.df.rename(columns={candidate: "Date"}, inplace=True)
                        break

            # Map optional/other columns if missing
            mappings = {
                PRODUCT_COLUMN: ["Product Name", "Product_Name", "Product_Title", "Item", "Product ID"],
                CATEGORY_COLUMN: ["Category Name", "Category_Name", "Sub-Category", "Sub_Category"],
                REGION_COLUMN: ["Region Name", "Region_Name", "Location", "State", "Country"],
                PROFIT_COLUMN: ["Profit Amount", "Profit_Amount", "Net Profit", "Net_Profit"],
                QUANTITY_COLUMN: ["Qty", "Quantity Ordered", "Units", "Order Quantity"],
                TARGET_COLUMN: ["Sales Amount", "Total Sales", "Revenue", "Amount"]
            }
            for std_col, candidates in mappings.items():
                if std_col not in self.df.columns:
                    for candidate in candidates:
                        if candidate in self.df.columns:
                            self.df.rename(columns={candidate: std_col}, inplace=True)
                            break

    def load_data(self, source):
        file_name = source.name if hasattr(source, "name") else str(source)
        extension = Path(file_name).suffix.lower()

        if extension == ".csv":
            if hasattr(source, "getvalue"):
                content = source.getvalue()
            elif hasattr(source, "read"):
                if hasattr(source, "seek"):
                    source.seek(0)
                content = source.read()
            else:
                content = source

            read_success = False
            for encoding in ["utf-8", "cp1252", "latin1", "utf-8-sig", "iso-8859-1"]:
                try:
                    if isinstance(content, bytes):
                        self.df = pd.read_csv(io.BytesIO(content), encoding=encoding)
                    else:
                        self.df = pd.read_csv(content, encoding=encoding)
                    read_success = True
                    break
                except Exception:
                    continue

            if not read_success:
                # Fallback with encoding_errors='replace' if all strict encodings fail
                try:
                    if isinstance(content, bytes):
                        self.df = pd.read_csv(io.BytesIO(content), encoding="utf-8", encoding_errors="replace")
                    else:
                        self.df = pd.read_csv(content, encoding="utf-8", encoding_errors="replace")
                except Exception as e:
                    raise ValueError(f"Failed to read CSV file: {e}")

        elif extension in (".xlsx", ".xls"):
            try:
                self.df = pd.read_excel(source)
            except Exception as e:
                raise ValueError(f"Failed to read Excel file: {e}")

        else:
            raise ValueError(f"Unsupported file format: {extension}")
        
        self._ensure_date_column()
        detector = SchemaDetector(self.df)
        self.schema = detector.build_schema()
        detector.save_dataset_config()

        import importlib
        import src.config
        importlib.reload(src.config)

        return self.df

    def get_dataset_info(self):
        if self.df is None:
            raise ValueError("No dataset loaded")
        info = {
            "rows": self.df.shape[0],
            "columns": self.df.shape[1],
            "column_names": self.df.columns.tolist(),
            "dtypes":self.df.dtypes.astype(str).to_dict(),
            "missing_values": self.df.isnull().sum().to_dict(),
            "duplicate_rows": int(self.df.duplicated().sum()),
            "memory_usage_mb": round(self.df.memory_usage(deep=True).sum() / (1024 ** 2),2),
        }

        return info

    def validate_columns(self):

        if self.df is None:
            raise ValueError("No dataset loaded")

        self._ensure_date_column()

        missing_column = [column for column in REQUIRED_COLUMNS if column not in self.df.columns]

        if missing_column:
            raise ValueError(f"Missing required columns: {','.join(missing_column)}")

        print("All columns are present")
        return True
        
    def clean_missing_values(self):
        if self.df is None:
            raise ValueError("No dataset loaded")
        self._ensure_date_column()
        date_col = self._get_date_col()
        if date_col in self.df.columns:
            self.df.dropna(subset=[date_col], inplace=True)
        print(f"shape after removing null values: {self.df.shape}")
        numeric_column = self.df.select_dtypes(include=[np.number]).columns.tolist()
        for column in numeric_column:
            self.df[column] = self.df[column].fillna(self.df[column].median())
        categorial_column = self.df.select_dtypes(include=["object"]).columns
        for column in categorial_column:
            if not self.df[column].mode().empty:
                self.df[column] = self.df[column].fillna(self.df[column].mode()[0])

        return self.df

    def remove_duplicates(self):
        if self.df is None:
            raise ValueError("No dataset loaded")

        duplicates_removed = self.df.duplicated().sum()

        self.df = self.df.drop_duplicates()

        return duplicates_removed

    def convert_date_columns(self):

        """
        Convert the Date column to datetime format.
        """

        if self.df is None:
            raise ValueError("No dataset loaded.")

        self._ensure_date_column()
        date_col = self._get_date_col()

        try:
            self.df[date_col] = pd.to_datetime(
                self.df[date_col],
                errors="coerce"
            )
        except Exception:
            raise ValueError(
                "Invalid date format found in the 'Date' column."
            )
        self.df = self.df.sort_values(date_col).reset_index(drop=True)

        return self.df
    
    def feature_engineering(self):
        """
        Create new features from the Date column.
        """

        if self.df is None:
            raise ValueError("No dataset loaded.")

        self._ensure_date_column()
        date_col = self._get_date_col()

        self.df["Year"] = self.df[date_col].dt.year
        self.df["Month"] = self.df[date_col].dt.month
        self.df["Day"] = self.df[date_col].dt.day
        self.df["Is_Weekend"] = (self.df[date_col].dt.dayofweek >= 5).astype(int)
        self.df["Quarter"] = self.df[date_col].dt.quarter

        return self.df

    def preprocess(self):
        """
        Execute the complete preprocessing pipeline.
        """

        if self.df is None:
            raise ValueError("No dataset loaded.")

        self._ensure_date_column()
        self.validate_columns()
        self.clean_missing_values()
        self.remove_duplicates()
        self.convert_date_columns()
        self.feature_engineering()

        return self.df