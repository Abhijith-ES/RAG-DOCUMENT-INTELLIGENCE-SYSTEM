import faiss
import pickle
import numpy as np
from pathlib import Path


def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings.astype('float32'))

    return index

def save_faiss_index(index, file_path):
    chunk = faiss.serialize_index(index)

    with open(file_path, "wb") as f:
        pickle.dump(chunk, f)

    print(f"FAISS Index Saved at {file_path}")

def load_faiss_index(file_path):
    with open(file_path, "rb") as f:
        chunk = pickle.load(f)
    
    return faiss.deserialize_index(chunk)

def save_metadata(metadata: list[dict], file_path):
    with open(file_path, "wb") as f:
        pickle.dump(metadata, f)

    print(f"Metadata Saved at {file_path}")

def load_metadata(file_path):
    with open(file_path, "rb") as f:
        metadata = pickle.load(f)

    return metadata