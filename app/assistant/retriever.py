from typing import List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.assistant.loader import load_and_chunk_documents


class Retriever:
    def __init__(self):
        self.documents: List[str] = load_and_chunk_documents()
        self.vectorizer = TfidfVectorizer()
        self.document_vectors = None

        if self.documents:
            self.document_vectors = self.vectorizer.fit_transform(self.documents)

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        min_score: float = 0.15
    ) -> List[str]:
        """
        Retrieve top_k relevant document chunks
        filtered by a minimum similarity score.
        """

        # Safety checks
        if not self.documents or self.document_vectors is None:
            return []

        # Vectorize query
        query_vector = self.vectorizer.transform([query])

        # Compute cosine similarity
        similarities = cosine_similarity(
            query_vector,
            self.document_vectors
        )[0]

        # Pair chunks with scores
        scored_chunks: List[Tuple[str, float]] = list(
            zip(self.documents, similarities)
            )
        relevant_chunks = [
                (chunk, score)
                for chunk, score in scored_chunks
                if score >= min_score
            ]

            # Sort by score descending
        relevant_chunks.sort(
                key=lambda item: item[1],
                reverse=True
            )

            # Debug (temporary)
        print("DEBUG — Top matches:")
        for chunk, score in relevant_chunks[:5]:
            print(f"Score: {score:.3f} | {chunk.splitlines()[0]}")


            # Return only text
        return [chunk for chunk, _ in relevant_chunks[:top_k]]