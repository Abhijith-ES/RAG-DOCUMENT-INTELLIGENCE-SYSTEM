def query_llm(prompt: str, groq_client) -> str:
    if not prompt.strip():
        raise ValueError(
            "The Prompt cannot be Empty."
        )
    
    response = groq_client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [
            {
                "role" : "user",
                "content" : prompt
            }
        ],
        temperature = 0.2
    )

    return response.choices[0].message.content

