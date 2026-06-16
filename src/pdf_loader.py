import fitz
from pathlib import Path


def extract_text_from_pdf(pdf_path: Path) -> list[dict] :
    doc = fitz.open(pdf_path)
    extracted_pages = []

    try:
        for page_num, page in enumerate(doc):
            text = page.get_text()
            
            if text.strip():
                extracted_pages.append(
                    {
                        "page_num" : page_num + 1,
                        "text" : text
                    }
                )

        return extracted_pages
    
    finally:
        doc.close()