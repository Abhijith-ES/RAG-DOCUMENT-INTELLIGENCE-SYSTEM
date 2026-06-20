from sentence_transformers import SentenceTransformer
import numpy as np


def load_embedding_model():
    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

def embed_text(texts : list[str], model : SentenceTransformer) -> np.ndarray:
    if not texts:
        raise ValueError("List Cannot be Empty!")

    return model.encode(texts, convert_to_numpy=True)