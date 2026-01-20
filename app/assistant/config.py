from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"


DATA_DIR = BASE_DIR / "data"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# LLM_MODEL_NAME = "llama3"



# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OPENAI_MODEL = "gpt-4o-mini"
