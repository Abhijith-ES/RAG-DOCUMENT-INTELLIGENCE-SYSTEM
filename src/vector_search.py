import numpy as np
from faiss import IndexFlatL2
from sentence_transformers import SentenceTransformer


def search_similar_chunks(query: str, 
                          index: IndexFlatL2, 
                          metadata: list[dict], 
                          embedding_model: SentenceTransformer, 
                          top_k : int=5
                          ) -> list[dict]:
    
    query_embedding = embedding_model.encode(query, convert_to_numpy=True)

    query_vector = np.array([query_embedding]).astype('float32')

    distances, indices = index.search(query_vector, top_k)

    results = []

    for idx in indices[0]:
        if idx == -1:
            continue

        results.append(
            metadata[idx]
        )

    return results