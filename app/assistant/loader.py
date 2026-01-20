from pathlib import Path
from typing import List, Dict
import re

from app.assistant.config import DATA_DIR, CHUNK_OVERLAP, CHUNK_SIZE


def load_text_files() -> List[Dict[str, str]]:
    """
    Load all .txt files and keep filename as metadata.
    """
    documents: List[Dict[str, str]] = []

    if not DATA_DIR.exists():
        return documents

    for file_path in DATA_DIR.glob("*.txt"):
        try:
            content = file_path.read_text(encoding="utf-8").strip()
            if content:
                documents.append({
                    "source": file_path.name,
                    "content": content
                })
        except Exception:
            continue

    return documents


def sentence_chunk_text(text: str) -> List[str]:
    """
    Split text into sentence-based chunks.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks: List[str] = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= CHUNK_SIZE:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def load_and_chunk_documents() -> List[str]:
    """
    Load documents, chunk them, and attach source metadata.
    """
    all_chunks: List[str] = []
    documents = load_text_files()

    for doc in documents:
        source = doc["source"]
        text = doc["content"]

        chunks = sentence_chunk_text(text)
        for chunk in chunks:
            tagged_chunk = f"[SOURCE: {source}]\n{chunk}"
            all_chunks.append(tagged_chunk)

    return all_chunks
