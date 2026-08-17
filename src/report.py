"""
report.py

Functional data analysis and PDF report generation module.
Calculates deterministic facts from DataFrames and exports PDF documents.
"""

import io
import datetime
import pandas as pd
import numpy as np

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

from src.ai_response import AIResponseGenerator


def get_dataset_overview(df: pd.DataFrame) -> dict:
    """
    Detect basic dataset overview metrics.
    """
    if df is None or df.empty:
        return {
            "rows": 0,
            "columns": 0,
            "column_names": [],
            "numeric_columns": [],
            "categorical_columns": [],
            "datetime_columns": []
        }

    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    categorical_columns = df.select_dtypes(include=["object", "category", "string"]).columns.tolist()
    datetime_columns = df.select_dtypes(include=["datetime64", "datetime"]).columns.tolist()

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "datetime_columns": datetime_columns
    }


def calculate_data_quality(df: pd.DataFrame) -> dict:
    """
    Calculate data quality metrics.
    """
    if df is None or df.empty:
        return {
            "total_rows": 0,
            "total_missing": 0,
            "missing_by_column": {},
            "duplicate_rows": 0,
            "complete_rows": 0,
            "completeness_pct": 0.0
        }

    total_rows = len(df)
    total_missing = int(df.isna().sum().sum())
    missing_by_col = {col: int(val) for col, val in df.isna().sum().to_dict().items() if val > 0}
    duplicate_rows = int(df.duplicated().sum())
    complete_rows = int(len(df.dropna()))
    completeness_pct = round((complete_rows / total_rows) * 100, 2) if total_rows > 0 else 0.0

    return {
        "total_rows": total_rows,
        "total_missing": total_missing,
        "missing_by_column": missing_by_col,
        "duplicate_rows": duplicate_rows,
        "complete_rows": complete_rows,
        "completeness_pct": completeness_pct
    }


def calculate_numeric_statistics(df: pd.DataFrame) -> dict:
    """
    Calculate descriptive statistics for numerical columns.
    """
    if df is None or df.empty:
        return {}

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if not numeric_cols:
        return {}

    stats = {}
    for col in numeric_cols:
        s = df[col].dropna()
        if len(s) == 0:
            continue
        stats[col] = {
            "count": int(s.count()),
            "mean": round(float(s.mean()), 2),
            "median": round(float(s.median()), 2),
            "min": round(float(s.min()), 2),
            "max": round(float(s.max()), 2),
            "std": round(float(s.std()), 2) if len(s) > 1 else 0.0
        }
    return stats


def calculate_categorical_insights(df: pd.DataFrame, max_cardinality: int = 50) -> dict:
    """
    Calculate categorical frequencies and aggregations against numerical columns.
    """
    if df is None or df.empty:
        return {}

    categorical_cols = df.select_dtypes(include=["object", "category", "string"]).columns.tolist()
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    insights = {}
    for cat_col in categorical_cols:
        unique_cnt = df[cat_col].nunique(dropna=True)
        if unique_cnt == 0 or unique_cnt > max_cardinality or unique_cnt == len(df):
            continue

        value_counts = {str(k): int(v) for k, v in df[cat_col].value_counts().head(5).to_dict().items()}
        dominant_cat = str(df[cat_col].mode().iloc[0]) if not df[cat_col].mode().empty else "N/A"

        grouped_stats = {}
        for num_col in numeric_cols:
            grp = (
                df.groupby(cat_col, observed=False)[num_col]
                .agg(["sum", "mean", "count"])
                .round(2)
            )
            top_performers = grp.sort_values(by="sum", ascending=False).head(3).to_dict(orient="index")
            bottom_performers = grp.sort_values(by="sum", ascending=True).head(3).to_dict(orient="index")
            grouped_stats[num_col] = {
                "top_3_by_sum": top_performers,
                "bottom_3_by_sum": bottom_performers
            }

        insights[cat_col] = {
            "unique_count": int(unique_cnt),
            "dominant_category": dominant_cat,
            "top_categories_count": value_counts,
            "metrics_breakdown": grouped_stats
        }

    return insights


def calculate_correlation_insights(df: pd.DataFrame) -> dict:
    """
    Calculate correlation matrix and highlight strongest relationships.
    """
    if df is None or df.empty:
        return {"correlation_matrix": {}, "strongest_positive": [], "strongest_negative": []}

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if len(numeric_cols) < 2:
        return {"message": "At least 2 numerical columns are required for correlation analysis."}

    corr_df = df[numeric_cols].corr().round(2)
    corr_dict = corr_df.to_dict()

    pairs = []
    for i in range(len(numeric_cols)):
        for j in range(i + 1, len(numeric_cols)):
            col1, col2 = numeric_cols[i], numeric_cols[j]
            val = float(corr_df.loc[col1, col2])
            if not np.isnan(val):
                pairs.append((col1, col2, val))

    pos_pairs = sorted([p for p in pairs if p[2] > 0], key=lambda x: x[2], reverse=True)[:3]
    neg_pairs = sorted([p for p in pairs if p[2] < 0], key=lambda x: x[2])[:3]

    return {
        "correlation_matrix": corr_dict,
        "strongest_positive": [{"pair": f"{p[0]} vs {p[1]}", "correlation": p[2]} for p in pos_pairs],
        "strongest_negative": [{"pair": f"{p[0]} vs {p[1]}", "correlation": p[2]} for p in neg_pairs]
    }


def get_forecast_context(session_state: dict) -> dict:
    """
    Retrieve existing forecast results from session state if available.
    """
    if "forecast_result" in session_state and session_state["forecast_result"] is not None:
        forecast_df = session_state["forecast_result"]
        if hasattr(forecast_df, "to_dict"):
            return {
                "available": True,
                "total_periods": len(forecast_df),
                "forecast_summary": forecast_df.head(10).to_dict(orient="records")
            }

    return {"available": False, "message": "No forecast generated yet."}


def build_report_context(
    overview: dict,
    data_quality: dict,
    numeric_statistics: dict,
    categorical_insights: dict,
    correlation_insights: dict,
    forecast_context: dict
) -> dict:
    """
    Combine all deterministic analysis results into a single context structure.
    """
    return {
        "overview": overview,
        "data_quality": data_quality,
        "numeric_statistics": numeric_statistics,
        "categorical_insights": categorical_insights,
        "correlations": correlation_insights,
        "forecast": forecast_context
    }


def generate_ai_report(report_context: dict) -> str:
    """
    Call Gemini to generate the human-friendly report from report context.
    """
    ai_gen = AIResponseGenerator()
    return ai_gen.generate_response(
        intent="report",
        question="Generate comprehensive business report",
        context=report_context
    )




def create_pdf(report_text: str, metadata: dict = None) -> bytes:
    """
    Convert Markdown report text into a professional PDF document using ReportLab.
    """
    if metadata is None:
        metadata = {}

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'DocH1',
        parent=styles['Heading2'],
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#2563EB'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading3'],
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#1F2937'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#374151'),
        spaceAfter=6
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Italic'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#6B7280'),
        spaceAfter=12
    )

    story = []

    # Title & Metadata Header
    story.append(Paragraph("📊 Executive Sales & Business Analytics Report", title_style))
    date_str = datetime.datetime.now().strftime("%B %d, %Y - %H:%M")
    meta_text = f"Generated: {date_str} | Platform: SalesPilot AI"
    story.append(Paragraph(meta_text, meta_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E5E7EB'), spaceAfter=12))

    # Process text line by line
    lines = report_text.split('\n')
    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue

        if line_str.startswith('# '):
            heading = line_str.lstrip('# ').strip()
            story.append(Paragraph(heading, h1_style))
        elif line_str.startswith('## '):
            heading = line_str.lstrip('# ').strip()
            story.append(Paragraph(heading, h2_style))
        elif line_str.startswith('### '):
            heading = line_str.lstrip('# ').strip()
            story.append(Paragraph(heading, h2_style))
        elif line_str.startswith('- ') or line_str.startswith('* '):
            bullet_text = "• " + line_str[2:].strip()
            story.append(Paragraph(bullet_text, body_style))
        else:
            clean_p = line_str.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            story.append(Paragraph(clean_p, body_style))

    doc.build(story)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data
