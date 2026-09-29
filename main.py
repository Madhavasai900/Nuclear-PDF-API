from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from pypdf import PdfReader
import io
import math

app = FastAPI(
    title="Nuclear PDF Extractor API - DEEP RDX EDITION",
    description="Extracts, chunks, and tokenizes ANY PDF for Vector Databases and LLMs.",
    version="Deep-Ghost-0.0001%"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_ai_chunks(text: str, chunk_size: int = 1000):
    """Splits text into RAG-ready blocks for Vector Databases."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        current_length += len(word) + 1
        if current_length > chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = len(word) + 1
        else:
            current_chunk.append(word)
            
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

@app.get("/")
def home():
    return {
        "message": "SYSTEM ONLINE. DEEP RDX PDF API is Active.",
        "trap_status": "$50/month Trap is READY."
    }

@app.get("/api/v1/extract-pdf")
def extract_pdf_data(url: str):
    """
    The Deep RDX Payload.
    Downloads PDF, extracts text, rips hidden metadata, chunks for RAG, and estimates LLM tokens.
    """
    if not url.startswith("http"):
        raise HTTPException(status_code=400, detail="Feed me a valid HTTP/HTTPS link to a PDF.")
        
    try:
        # 1. Download PDF to Memory
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Target server blocked the request. Status {response.status_code}")
            
        pdf_file = io.BytesIO(response.content)
        reader = PdfReader(pdf_file)
        
        # 2. Rip Hidden Metadata
        meta = reader.metadata
        hidden_data = {
            "author": meta.author if meta and meta.author else "Unknown",
            "creator": meta.creator if meta and meta.creator else "Unknown",
            "producer": meta.producer if meta and meta.producer else "Unknown"
        }
        
        # 3. Rip and Clean Text
        total_pages = len(reader.pages)
        full_text = ""
        
        for i in range(total_pages):
            text = reader.pages[i].extract_text()
            if text:
                full_text += text + "\n\n"
                
        cleaned_text = full_text.strip()
        
        # 4. Deep AI Processing (The Money Maker)
        ai_chunks = create_ai_chunks(cleaned_text, chunk_size=1200)
        estimated_tokens = math.ceil(len(cleaned_text.split()) * 1.3) # Rough LLM token formula
                
        return {
            "status": "success",
            "source_url": url,
            "deep_metadata": hidden_data,
            "ai_analysis": {
                "total_pages": total_pages,
                "character_count": len(cleaned_text),
                "estimated_llm_tokens": estimated_tokens,
                "vector_ready_chunks": len(ai_chunks)
            },
            "rag_chunks": ai_chunks,
            "raw_text": cleaned_text
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deep Ghost Mode Error: {str(e)}")
