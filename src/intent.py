import re
from typing import Dict


class IntentDetector:
    
    # Detects the intent of a user's query

    FORECAST = "forecast"
    ANALYSIS = "analysis"
    BUSINESS_ADVICE = "business_advice"
    SUMMARY = "summary"
    VISUALIZATION = "visualization"
    GENERAL_CHAT = "general_chat"
    UNKNOWN = "unknown"

    # Keywords (Generic, dataset-independent)

    INTENT_KEYWORDS = {

        FORECAST: [
            "forecast",
            "predict",
            "prediction",
            "future",
            "next month",
            "next quarter",
            "next year",
            "next week",
            "next day",
            "estimate",
            "estimated",
            "expected",
            "projection",
            "forecasting",
            "tomorrow"
        ],

        ANALYSIS: [
            "best",
            "top",
            "performing",
            "performs",
            "performance",
            "underperforming",
            "worst",
            "highest",
            "lowest",
            "most",
            "least",
            "compare",
            "comparison", "across",
            "trend",
            "trends",
            "leader",
            "leaders",
            "area",
            "areas",
            "group",
            "groups",
            "segment",
            "segments",
            "dimension",
            "dimensions",
            "breakdown",
            "correlated",
            "correlation",
            "correlations",
            "doing well",
            "losing money",
            "revenue",
            "value",
            "count",
            "average",
            "total",
            "distribution",
            "which",
            "where",
            "what",
            "how",
            "show",
            "display",
            "analysis",
            "analyze",
            "statistics",
            "stats",
            "metrics",
            "performer",
            "performers"
        ],

        BUSINESS_ADVICE: [
            "recommend",
            "recommendation",
            "suggest",
            "suggestion",
            "improve",
            "increase",
            "decrease",
            "growth",
            "strategy",
            "optimize",
            "advice",
            "reason",
            "why",
            "help me",
            "business",
            "focus",
            "opportunity"
        ],

        SUMMARY: [
            "summary",
            "summarize",
            "overview",
            "describe",
            "dataset summary"
        ],

        VISUALIZATION: [
            "chart",
            "plot",
            "graph",
            "visualize",
            "visualization"
        ],

        GENERAL_CHAT: [
            "hello",
            "hi",
            "hey",
            "good morning",
            "good evening",
            "thanks",
            "thank you",
            "who are you",
            "help"
        ]
    }


    def __init__(self):

        self.last_intent = None
        self.last_confidence = 0.0


    def clean_query(self, query: str) -> str:
        """
        Normalize the user query.
        """

        query = query.lower().strip()

        query = re.sub(r"[^\w\s]", "", query)

        query = re.sub(r"\s+", " ", query)

        return query


    def calculate_confidence(self, query: str, keywords: list) -> float:
        
        matches = 0

        for keyword in keywords:

            if keyword in query:
                matches += 1

        if matches == 0:
            return 0.0

        # Cap confidence at 1.0
        confidence = min(
            0.35 + (matches * 0.25),
            1.0
        )

        return round(confidence, 2)

    
    def detect(self, query: str) -> Dict:

        query = self.clean_query(query)

        best_intent = self.UNKNOWN
        highest_confidence = 0.0

        for intent, keywords in self.INTENT_KEYWORDS.items():

            confidence = self.calculate_confidence(
                query,
                keywords
            )

            if confidence > highest_confidence:

                highest_confidence = confidence
                best_intent = intent

        self.last_intent = best_intent
        self.last_confidence = highest_confidence

        return {

            "intent": best_intent,
            "confidence": highest_confidence,
            "entities": self._extract_entities(query)

        }


    def needs_llm(
        self,
        confidence_threshold: float = 0.55
    ) -> bool:
        """
        Decide whether Gemini should classify
        the intent.

        Returns True if confidence is low.
        """

        return self.last_confidence < confidence_threshold


    def reset(self):
        """
        Reset detector state.
        """

        self.last_intent = None
        self.last_confidence = 0.0

    def _extract_entities(self, query: str):
        entities = {
            "periods" : 12,
            "frequency": "M"
        }
        
        query = self.clean_query(query)
        if "tomorrow" in query or "tommorrow" in query:
            return {
                "periods" : 1,
                "frequency" : "D"
            }
        if "next year" in query:
            return {
                "periods": 12,
                "frequency" : "Y"
            }
        if "next week" in query:
            return {
                "periods": 7,
                "frequency" : "W"
            }
        if "next month" in query:
            return {
                "periods": 1,
                "frequency" : "M"
            }
        pattern = (r"(?:next\s+)?"
        r"(\d+)\s*"
        r"(day|days|week|weeks|month|months|"
        r"quarter|quarters|year|years)")
        match = re.search(pattern, query)
        if match:
             periods = int(match.group(1))
             unit = match.group(2)

             if unit in ["day", "days"]:
                frequency = "D"

             elif unit in ["week", "weeks"]:
                frequency = "W"

             elif unit in ["month", "months"]:
                frequency = "M"

             elif unit in ["quarter", "quarters"]:
                frequency = "Q"

             elif unit in ["year", "years"]:
                frequency = "Y"

             else:
                frequency = "M"

             entities["periods"] = periods
             entities["frequency"] = frequency

        return entities

            
