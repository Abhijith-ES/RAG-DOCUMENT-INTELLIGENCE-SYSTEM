def create_chunks(pages: list, 
                  chunk_size=500, chunk_overlap=50) -> list[dict]:
    
    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )
    
    chunk_list = []
    step = chunk_size - chunk_overlap

    for page in pages:
        page_no = page["page_num"]
        text = page["text"]

        chunk_id = 1

        for start_idx in range(0, len(text), step):
            chunk_text = text[start_idx: (start_idx + chunk_size)]

            if chunk_text.strip():
                chunk_list.append({
                    "page_num" : page_no,
                    "chunk_id" : chunk_id,
                    "chunk" : chunk_text
                })

                chunk_id+=1
    
    return chunk_list
    
