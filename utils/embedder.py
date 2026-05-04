import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddingHandler:
    def __init__(self):
        print("TF-IDF Search ready — free, no download!")
        self.chunks_store = {}
        self.vectorizers = {}
        self.matrices = {}

    def process_and_store(self, transcript: str, session_id: str):
        chunks = self._chunk_transcript(transcript)
        vectorizer = TfidfVectorizer(stop_words='english')
        matrix = vectorizer.fit_transform(chunks)
        self.chunks_store[session_id] = chunks
        self.vectorizers[session_id] = vectorizer
        self.matrices[session_id] = matrix
        print(f"Stored {len(chunks)} chunks for session {session_id}")

    def retrieve(self, query: str, session_id: str, top_k: int = 5) -> str:
        if session_id not in self.chunks_store:
            raise ValueError("Session not found.")
        vectorizer = self.vectorizers[session_id]
        matrix = self.matrices[session_id]
        chunks = self.chunks_store[session_id]
        query_vec = vectorizer.transform([query])
        scores = cosine_similarity(query_vec, matrix).flatten()
        top_indices = scores.argsort()[-top_k:][::-1]
        top_chunks = [chunks[i] for i in top_indices]
        return "\n\n---\n\n".join(top_chunks)

    def _chunk_transcript(self, transcript: str, chunk_size: int = 400, overlap: int = 50) -> list:
        words = transcript.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
        return chunks

    def cleanup_session(self, session_id: str):
        for store in [self.chunks_store, self.vectorizers, self.matrices]:
            if session_id in store:
                del store[session_id]