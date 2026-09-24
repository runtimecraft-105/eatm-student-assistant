import re


class QueryRouter:

    EATM_KEYWORDS = [
        "eatm",
        "college",
        "campus",
        "hostel",
        "admission",
        "admissions",
        "placement",
        "placements",
        "examination",
        "exam",
        "notice",
        "notices",
        "department",
        "departments",
        "faculty",
        "library",
        "canteen",
        "transport",
        "fees",
        "regulation",
        "regulations",
    ]

    FOLLOW_UP_PHRASES = [
        "which one",
        "which ones",
        "what about",
        "how about",
        "that one",
        "this one",
        "those",
        "these",
        "it",
        "they",
        "them",
        "more about",
        "tell me more",
        "explain more",
    ]

    @classmethod
    def is_eatm_query(
        cls,
        question: str,
        history: list | None = None
    ) -> bool:

        question_lower = question.lower()

        # Direct EATM-related question
        for keyword in cls.EATM_KEYWORDS:

            pattern = rf"\b{re.escape(keyword)}\b"

            if re.search(pattern, question_lower):
                return True

        # Follow-up question related to previous context
        if history:

            for phrase in cls.FOLLOW_UP_PHRASES:

                if phrase in question_lower:
                    return True

            previous_messages = history[-4:]

            previous_text = " ".join(
                message.get("content", "")
                for message in previous_messages
            ).lower()

            for keyword in cls.EATM_KEYWORDS:

                pattern = rf"\b{re.escape(keyword)}\b"

                if re.search(pattern, previous_text):
                    return True

        return False