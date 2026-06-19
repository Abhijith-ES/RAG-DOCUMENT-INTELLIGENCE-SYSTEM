from src.vector_search import search_similar_chunks
from src.prompt import build_prompt
from src.llm import query_llm

def generate_answer(query : str, index, 
                    metadata : list[dict], embedding_model, 
                    groq_client):
    
    results = search_similar_chunks(query, index, metadata, embedding_model, top_k=5)

    if not results:
        return ("I couldn't find that information in the document.")

    prompt = build_prompt(query, results)

    answer = query_llm(prompt, groq_client)

    return answer


