"""
ai_response.py

Handles all interactions with Google Gemini.
"""

import os
import json

from google import genai
from dotenv import load_dotenv

from src.prompts import (
    SYSTEM_PROMPT,
    FORECAST_PROMPT,
    ANALYSIS_PROMPT,
    INSIGHT_PROMPT,
    SUMMARY_PROMPT,
    VISUALIZATION_PROMPT,
    GENERAL_CHAT_PROMPT,
    ERROR_PROMPT,
    NO_DATASET_PROMPT,
    REPORT_PROMPT
)

load_dotenv()


class AIResponseGenerator:

    def __init__(
        self,
        model_name="gemini-2.5-flash"
    ):
        """
        Initialize Gemini client.
        """

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables."
            )

        self.client = genai.Client(api_key=api_key)

        self.model_name = model_name

    # -----------------------------------------------------
    # Prompt Builder
    # -----------------------------------------------------

    def _build_prompt(
        self,
        intent,
        question,
        context=None
    ):
        if not isinstance(context, dict):
            context = {}

        if intent == "forecast":

            return SYSTEM_PROMPT + "\n\n" + FORECAST_PROMPT.format(
                dataset_summary=context.get("dataset_summary", ""),
                forecast_result=context.get("forecast_result", ""),
                question=question
            )

        elif intent in ["analysis", "business_advice", "insight"]:

            analysis_res = context.get("analysis_result", context.get("business_context", ""))
            return SYSTEM_PROMPT + "\n\n" + ANALYSIS_PROMPT.format(
                dataset_summary=context.get("dataset_summary", ""),
                analysis_result=analysis_res,
                question=question
            )

        elif intent == "report":

            report_ctx = context.get("report_context", context)
            if isinstance(report_ctx, dict):
                report_str = json.dumps(report_ctx, indent=2, default=str)
            else:
                report_str = str(report_ctx)

            return SYSTEM_PROMPT + "\n\n" + REPORT_PROMPT.format(
                report_context=report_str
            )

        elif intent == "summary":

            return SYSTEM_PROMPT + "\n\n" + SUMMARY_PROMPT.format(
                dataset_summary=context.get("dataset_summary", "")
            )

        elif intent == "visualization":

            return SYSTEM_PROMPT + "\n\n" + VISUALIZATION_PROMPT.format(
                chart_summary=context.get("chart_summary", context.get("analysis_result", "")),
                question=question
            )

        elif intent == "no_dataset":

            return SYSTEM_PROMPT + "\n\n" + NO_DATASET_PROMPT

        else:

            return SYSTEM_PROMPT + "\n\n" + GENERAL_CHAT_PROMPT.format(
                question=question
            )


    # -----------------------------------------------------
    # Gemini API Call
    # -----------------------------------------------------

    def _call_gemini(
        self,
        prompt
    ):
        """
        Send prompt to Gemini.
        """

        try:

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )

            return response.text.strip()

        except Exception as e:

            return ERROR_PROMPT.format(
                error=str(e)
            )

    # -----------------------------------------------------
    # Public Methods
    # -----------------------------------------------------

    def generate_response(
        self,
        intent,
        question,
        context=None
    ):
        """
        Generate AI response.
        """

        if context is None:
            context = {}

        prompt = self._build_prompt(
            intent=intent,
            question=question,
            context=context
        )

        response = self._call_gemini(
            prompt
        )

        return response

    def generate_report_response(
        self,
        report_context
    ):
        """
        Generate AI report response from structured report context.
        """

        return self.generate_response(
            intent="report",
            question="Generate comprehensive business report",
            context=report_context
        )