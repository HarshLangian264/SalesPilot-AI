# src/config.py

import importlib
import src.dataset_config as dataset_config

try:
    importlib.reload(dataset_config)
except Exception:
    pass

# Dynamically set column variables from dataset_config with fallbacks if None
DATE_COLUMN = getattr(dataset_config, "DATE_COLUMN", None) or "Date"
TARGET_COLUMN = getattr(dataset_config, "TARGET_COLUMN", None) or "Sales"
CATEGORY_COLUMN = getattr(dataset_config, "CATEGORY_COLUMN", None) or "Category"
REGION_COLUMN = getattr(dataset_config, "REGION_COLUMN", None) or "Region"
PRODUCT_COLUMN = getattr(dataset_config, "PRODUCT_COLUMN", None) or "Product"
PROFIT_COLUMN = getattr(dataset_config, "PROFIT_COLUMN", None) or "Profit"
QUANTITY_COLUMN = getattr(dataset_config, "QUANTITY_COLUMN", None) or "Quantity"

# REQUIRED_COLUMNS dynamically generated from required dataset fields
REQUIRED_COLUMNS = [col for col in [DATE_COLUMN, TARGET_COLUMN] if col is not None]

OPTIONAL_COLUMNS = [
    col for col in [PRODUCT_COLUMN, CATEGORY_COLUMN, REGION_COLUMN, QUANTITY_COLUMN, PROFIT_COLUMN]
    if col is not None
]

SUPPORTED_FILE_TYPES = [
    ".csv",
    ".xlsx",
    ".xls"
]

