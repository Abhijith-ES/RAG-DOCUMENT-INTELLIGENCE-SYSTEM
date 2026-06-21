from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from groq import Groq
import os
import uuid
from pathlib import Path

from src.embeddings import load_embedding_model
from src.ingestion_pipeline import process_document
from src.rag_pipeline import generate_answer
from src.schemas import UploadResponse, AskRequest, AskResponse
from src.vector_store import load_faiss_index, load_metadata


load_dotenv()

upload_dir = Path("uploads")
upload_dir.mkdir(
    exist_ok=True,
    parents=True
)

vector_db_path = Path("vector_db")
vector_db_path.mkdir(
    exist_ok=True,
    parents=True
)

@asynccontextmanager
async def lifespan(app : FastAPI):
    if os.getenv("GROQ_API_KEY"):
        app.state.groq_client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
            )
    else:
        raise RuntimeError("Groq API Key Not Found.")
    
    app.state.embedding_model = load_embedding_model()
    yield

app = FastAPI(lifespan=lifespan)

@app.get('/')
def home():
    return {
        "message" : "RAG System is Running."
    }

@app.get('/health')
def health_check():
    return {
        'status' : 'healthy'
    }

@app.post('/upload', response_model=UploadResponse )
def upload_document(request : Request, file : UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF Files are supported."
        )
    
    document_id = str(uuid.uuid4())[:8]
    pdf_path = upload_dir / f"{document_id}.pdf"

    with open(pdf_path, "wb") as f:
        contents = file.file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )
        f.write(contents)

    try:
        result = process_document(
            pdf_path=pdf_path,
            document_id=document_id,
            embedding_model=request.app.state.embedding_model
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
    return UploadResponse(
        document_id=result["document_id"],
        message = "Document processed successfully.",
        num_chunks=result["chunks"]
    )

@app.post('/ask', response_model=AskResponse)
def ask_question(user_query : AskRequest, request : Request):
    
    index_path = vector_db_path / f"{user_query.document_id}.faiss"
    if not index_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )
    index = load_faiss_index(index_path)

    metadata_path = vector_db_path / f"{user_query.document_id}.pkl"
    if not metadata_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )
    metadata = load_metadata(metadata_path)

    try:
        answer = generate_answer(
            query=user_query.query,
            index=index,
            metadata=metadata,
            embedding_model=request.app.state.embedding_model,
            groq_client=request.app.state.groq_client
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return AskResponse(answer=answer)