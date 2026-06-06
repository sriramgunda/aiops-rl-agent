# Retriever for incident documents using FAISS and Sentence Transformers
import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

class IncidentRetriever:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.documents = []
        self.index = None

    def load(self, path):
        print(f"Loading documents from {path}...")
        with open(path, "r") as f:
            self.documents = json.load(f)

        texts = [d["symptoms"] for d in self.documents]
        # Compute embeddings for the documents
        embeddings = self.model.encode(texts)
        embeddings = np.array(embeddings, dtype=np.float32)

        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(embeddings)

    def retrieve(self, query):
        emb = self.model.encode([query])
        emb = np.array(emb, dtype=np.float32)

        distances, indexes = self.index.search(emb, 1)
        idx = indexes[0][0]
        print(f"Retrieved document index: {idx}, distance: {distances[0][0]}")
        return {"document": self.documents[idx], "distance": float(distances[0][0])}