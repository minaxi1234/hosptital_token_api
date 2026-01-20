import subprocess


def generate_answer(question: str, context: str = "") -> str:
    """
    Generate an answer using Ollama.
    The model MUST use only provided hospital information.
    """

    prompt = f"""
You are a hospital information assistant.

STRICT RULES (YOU MUST FOLLOW):
- Use ONLY the hospital information given below.
- Do NOT use general knowledge.
- Do NOT guess or assume anything.
- Do NOT invent services, food, shops, or facilities.
- If the answer is NOT clearly present in the hospital information,
  reply EXACTLY with:
  "I don't have information about that."

Hospital Information:
{context}

Question:
{question}

Answer:
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "tinyllama"],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=30
        )

        if result.stderr:
            print("Ollama stderr:", result.stderr)

        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        return "LLM error: process timed out."

    except Exception as e:
        return f"LLM error: {str(e)}"
