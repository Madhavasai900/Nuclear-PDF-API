from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from pypdf import PdfReader
import io

app = FastAPI(
    title="Nuclear PDF Extractor API",
    description="Extracts clean text from ANY PDF link on the internet for AI Agents.",
    version="Ghost-0.0001%"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "SYSTEM ONLINE. Nuclear PDF API is Active.",
        "trap_status": "$30/month Trap is READY.",
        "elite_level": "0.0001%"
    }

@app.get("/api/v1/extract-pdf")
def extract_pdf_data(url: str):
    """
    Takes a direct link to a PDF file, downloads it in memory,
    and rips out all the text page by page.
    """
    if not url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL format. Provide a valid HTTP/HTTPS link to a PDF.")
        
    try:
        # 1. Download the PDF into memory (No disk saving needed, faster)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to download PDF. Target server returned status {response.status_code}")
            
        # 2. Read the PDF from memory
        pdf_file = io.BytesIO(response.content)
        reader = PdfReader(pdf_file)
        
        total_pages = len(reader.pages)
        full_text = ""
        
        # 3. Rip the text
        for i in range(total_pages):
            page = reader.pages[i]
            text = page.extract_text()
            if text:
                full_text += text + "\n\n"
                
        return {
            "status": "success",
            "metadata": {
                "total_pages": total_pages,
                "source_url": url,
                "extracted_characters": len(full_text)
            },
            "text": full_text.strip()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ghost Mode Error: {str(e)}")
