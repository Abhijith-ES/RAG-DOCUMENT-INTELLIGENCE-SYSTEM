def build_prompt(query:str, retrieved_chunks : list[dict]):
    context="\n\n".join(
        chunk['chunk']
        for chunk in retrieved_chunks
    )

    prompt = f"""
You are a document intelligence assistant.

Only answer using the provided context.

If the answer is not present in the context, say:
"I couldn't find that information in the document."

Context:
{context}

Question:
{query}

Answer:
"""
    return prompt