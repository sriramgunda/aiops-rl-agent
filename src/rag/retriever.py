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

        texts = []
        for doc in self.documents:
            texts.append(
                f"""
                incident {doc['incident']}
                symptoms {doc['symptoms']}
                root cause {doc['root_cause']}
                recommended action {doc['recommended_action']}
                """
            )
        
        # Compute embeddings for the documents
        embeddings = self.model.encode(texts)
        embeddings = np.array(embeddings, dtype=np.float32)

        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(embeddings)

    def retrieve(self, query, top_k=2):
        if query == "" or query is None:
            return {'document':
                    {'incident': 'no_incident',
                     'symptoms': 'nothing',
                     'root_cause': 'false alert',
                     'recommended_action': 'no_action'},
                     'score': 0.0}
        emb = self.model.encode([query])
        emb = np.array(emb, dtype=np.float32)

        distances, indexes = self.index.search(emb, top_k)

        # print("\n===================")
        # print(f"QUERY: {query}")

        # print("\nTOP RESULTS:")
        results = []
        for rank,(idx,dist) in enumerate(zip(indexes[0], distances[0])):
            doc = self.documents[idx]

            # custom scoring the docs
            score = 1/(1 + dist)

            # add the doc scores to results
            results.append([score, doc])
            #print(f"{rank+1}. {self.documents[idx]['incident']} (distance={dist:.4f}) (score={score:.4f})" )
        
        # sort the results
        results.sort(reverse=True, key=lambda x:x[0])
        #print(f"results: {results}")
        #print(f"indexes: {indexes}")

        #best_idx = indexes[0][0]
        #print(f"Retrieved best document: {self.documents[best_idx]}, distance: {float(distances[0][0])}")
        #return {"document": self.documents[best_idx], "distance": float(distances[0][0])}

        best_idx = results[0]
        #print(f"Retrieved best document: {best_idx[1]}, score: {float(best_idx[0])}")
        return {"document": best_idx[1], "score": float(best_idx[0])}