# This module implements a simple Retrieval-Augmented Generation (RAG) engine for AIOps.
# It uses a sentence transformer model to encode incident symptoms and a FAISS index for efficient retrieval

import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class RAGEngine:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.docs = []

    def load_documents(self,path):
        # Load documents from a JSON file, encode their symptoms, and build a FAISS index for retrieval
        with open(path,"r") as f:
            self.docs=json.load(f)
        texts = [
            d["symptoms"] for d in self.docs
        ]
        embeddings = self.model.encode(texts)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings))
        print(f"Loaded {len(self.docs)} documents into the RAG engine.")


    def retrieve(self, query, k=2):
        # Encode the query symptoms and retrieve the top-k most similar documents from the FAISS index
        query_emb = self.model.encode([query])
        D,I = self.index.search(np.array(query_emb), k)
        print(f"Retrieved documents for query: '{query}'")
        return [self.docs[i] for i in I[0]]