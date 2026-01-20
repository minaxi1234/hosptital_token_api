from typing import Dict, List
import logging
import re

from app.assistant.retriever import Retriever
from app.assistant.llm import generate_answer

logger = logging.getLogger(__name__)


HOSPITAL_KEYWORDS = [
    "hospital", "doctor", "doctors", "nurse", "nurses",
    "opd", "timing", "timings", "department", "specialty",
    "appointment", "token", "tokens", "emergency",
    "cardiology", "pediatric", "gynecology",
    "patient", "registration", "clinic", "ward"
]


class AssistantService:
    def __init__(self):
        self.retriever = Retriever()
        self.cache: Dict[str, str] = {}

    def _is_hospital_related(self, question: str) -> bool:
        q = question.lower()
        return any(keyword in q for keyword in HOSPITAL_KEYWORDS)

    def ask(self, question: str) -> Dict[str, str]:

        if question in self.cache:
            return {
                "question": question,
                "answer": self.cache[question]
            }

        # 🚨 HARD DOMAIN BLOCK (THIS IS THE REAL FIX)
        if not self._is_hospital_related(question):
            answer = "I don't have information about that."
            self.cache[question] = answer
            return {
                "question": question,
                "answer": answer
            }

        contexts: List[str] = self.retriever.retrieve(question)

        if not contexts:
            answer = "I don't have information about that."
        else:
            context_text = "\n".join(contexts)

            try:
                answer = generate_answer(
                    question=question,
                    context=context_text
                )
            except Exception:
                answer = "The assistant is temporarily unavailable."

        self.cache[question] = answer

        return {
            "question": question,
            "answer": answer
        }
