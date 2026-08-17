import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.config import DATE_COLUMN,TARGET_COLUMN,CATEGORY_COLUMN,PROFIT_COLUMN,QUANTITY_COLUMN,REGION_COLUMN,PRODUCT_COLUMN

class datavisualizer:
    def __init__(self, df):
        self.df = df

    def _empty_fig(self, message):
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            template="plotly_white"
        )
        return fig

    def get_kpis(self):
        if self.df is None:
            raise ValueError("No data is loaded")

        total_sales = round(self.df[TARGET_COLUMN].sum(), 2) if TARGET_COLUMN in self.df.columns else 0.0
        total_profit = round(self.df[PROFIT_COLUMN].sum(), 2) if PROFIT_COLUMN in self.df.columns else 0.0
        total_orders = len(self.df)
        average_sales = round(self.df[TARGET_COLUMN].mean(), 2) if TARGET_COLUMN in self.df.columns else 0.0
        total_quantity = int(self.df[QUANTITY_COLUMN].sum()) if QUANTITY_COLUMN in self.df.columns else 0
        average_profit = round(self.df[PROFIT_COLUMN].mean(), 2) if PROFIT_COLUMN in self.df.columns else 0.0

        kpis = {
            "total_sales": total_sales,
            "total_profit": total_profit,
            "total_orders": total_orders,
            "average_sales": average_sales,
            "total_quantity": total_quantity,
            "average_profit": average_profit
        }
        return kpis

    def plot_sales_trend(self):
        if self.df is None:
            raise ValueError("No dataset available.")

        date_col = DATE_COLUMN if DATE_COLUMN in self.df.columns else ("Date" if "Date" in self.df.columns else None)
        if not date_col or TARGET_COLUMN not in self.df.columns:
            return self._empty_fig("Date or Sales column not found in dataset")

        sales_trend = (
            self.df.groupby(date_col)[TARGET_COLUMN]
            .sum()
            .reset_index()
        )

        fig = px.line(
            sales_trend,
            x=date_col,
            y=TARGET_COLUMN,
            title="Sales Trend Over Time",
            markers=True
        )

        fig.update_layout(
            xaxis_title=date_col,
            yaxis_title=TARGET_COLUMN,
            template="plotly_white"
        )

        return fig

    def plot_monthly_sales(self):
        if self.df is None:
            raise ValueError("No dataset available.")

        if "Year" not in self.df.columns or "Month" not in self.df.columns or TARGET_COLUMN not in self.df.columns:
            return self._empty_fig("Year/Month data not found in dataset")

        monthly_sales = (
            self.df.groupby(["Year", "Month"])[TARGET_COLUMN]
            .sum()
            .reset_index()
        )

        monthly_sales["Month-Year"] = (
            monthly_sales["Year"].astype(str)
            + "-"
            + monthly_sales["Month"].astype(str).str.zfill(2)
        )

        fig = px.line(
            monthly_sales,
            x="Month-Year",
            y=TARGET_COLUMN,
            title="Monthly Sales Trend",
            markers=True
        )

        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Sales",
            template="plotly_white"
        )

        return fig

    def plot_sales_by_category(self):
        if self.df is None:
            raise ValueError("No dataset available.")

        if CATEGORY_COLUMN not in self.df.columns or TARGET_COLUMN not in self.df.columns:
            return self._empty_fig(f"'{CATEGORY_COLUMN}' column not found in dataset")

        category_sales = (
            self.df.groupby(CATEGORY_COLUMN)[TARGET_COLUMN]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig = px.bar(
            category_sales,
            x=CATEGORY_COLUMN,
            y=TARGET_COLUMN,
            title="Sales by Category",
            text_auto=".2s"
        )

        fig.update_layout(
            xaxis_title=CATEGORY_COLUMN,
            yaxis_title=TARGET_COLUMN,
            template="plotly_white"
        )

        return fig

    def plot_sales_by_region(self):
        if self.df is None:
            raise ValueError("No dataset available.")

        if REGION_COLUMN not in self.df.columns or TARGET_COLUMN not in self.df.columns:
            return self._empty_fig(f"'{REGION_COLUMN}' column not found in dataset")

        region_sales = (
            self.df.groupby(REGION_COLUMN)[TARGET_COLUMN]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig = px.bar(
            region_sales,
            x=TARGET_COLUMN,
            y=REGION_COLUMN,
            orientation="h",
            title="Sales by Region",
            text_auto=".2s"
        )

        fig.update_layout(
            xaxis_title="Total Sales",
            yaxis_title="Region",
            template="plotly_white"
        )

        return fig

    def plot_top_products(self):
        if self.df is None:
            raise ValueError("No dataset available.")

        if PRODUCT_COLUMN not in self.df.columns or TARGET_COLUMN not in self.df.columns:
            return self._empty_fig(f"'{PRODUCT_COLUMN}' column not found in dataset")

        top_products = (
            self.df.groupby(PRODUCT_COLUMN)[TARGET_COLUMN]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig = px.bar(
            top_products,
            x=TARGET_COLUMN,
            y=PRODUCT_COLUMN,
            orientation="h",
            title="Top 10 Products by Sales",
            text_auto=".2s"
        )

        fig.update_layout(
            xaxis_title=TARGET_COLUMN,
            yaxis_title=PRODUCT_COLUMN,
            template="plotly_white"
        )

        fig.update_yaxes(categoryorder="total ascending")

        return fig

    def plot_profit_distribution(self):
        if self.df is None:
            raise ValueError("No dataset available.")

        if PROFIT_COLUMN not in self.df.columns:
            return self._empty_fig(f"'{PROFIT_COLUMN}' column not found in dataset")

        fig = px.histogram(
            self.df,
            x=PROFIT_COLUMN,
            nbins=30,
            title="Profit Distribution"
        )

        fig.update_layout(
            xaxis_title="Profit",
            yaxis_title="Number of Orders",
            template="plotly_white"
        )

        return fig

    def plot_sales_by_year(self):
        if self.df is None:
            raise ValueError("No dataset available.")

        if "Year" not in self.df.columns or TARGET_COLUMN not in self.df.columns:
            return self._empty_fig("Yearly data not found in dataset")

        sales_by_year = (
            self.df.groupby("Year")[TARGET_COLUMN]
            .sum()
            .reset_index()
        )

        fig = px.line(
            sales_by_year,
            x="Year",
            y=TARGET_COLUMN,
            title="Sales by Year",
            markers=True
        )

        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Total Sales",
            template="plotly_white"
        )

        return fig

    def plot_correlation_heatmap(self):
        if self.df is None:
            raise ValueError("No dataset available.")

        numeric_columns = [
            "Sales",
            "Profit",
            "Quantity",
            "Discount"
        ]

        available_columns = [
            col for col in numeric_columns
            if col in self.df.columns
        ]

        if len(available_columns) < 2:
            return self._empty_fig("Not enough numerical columns for correlation heatmap")

        corr_matrix = self.df[available_columns].corr()

        fig = px.imshow(
            corr_matrix,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            title="Correlation Heatmap",
            aspect="auto"
        )

        fig.update_layout(
            template="plotly_white"
        )

        return fig
