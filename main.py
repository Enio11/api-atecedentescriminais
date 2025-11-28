from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from scraper import search_tjsp, search_portal_transparencia
from database import init_db, log_request, get_total_requests
import logging

# Initialize DB
init_db()

app = FastAPI(
    title="TJSP Criminal Records API",
    description="API to check criminal records (antecedents) on TJSP by CPF/CNPJ.",
    version="1.0.0"
)

def format_document(doc: str) -> str:
    """Formats a string of digits into CPF or CNPJ format."""
    clean = "".join(filter(str.isdigit, doc))
    
    if len(clean) == 11: # CPF
        return f"{clean[:3]}.{clean[3:6]}.{clean[6:9]}-{clean[9:]}"
    elif len(clean) == 14: # CNPJ
        return f"{clean[:2]}.{clean[2:5]}.{clean[5:8]}/{clean[8:12]}-{clean[12:]}"
    
    return doc # Return original if not 11 or 14 digits

class SearchRequest(BaseModel):
    document: str

from typing import Optional

class Process(BaseModel):
    number: str
    degree: str
    link: str
    classe: Optional[str] = None
    area: Optional[str] = None
    assunto: Optional[str] = None
    data_distribuicao: Optional[str] = None
    juiz: Optional[str] = None
    valor_acao: Optional[str] = None
    partes: list[str] = []
    movimentacoes: list[str] = []

class SearchResponse(BaseModel):
    document: str
    records_count: int
    processes: list[Process] = []
    names: list[str] = []
    status: str

@app.get("/")
def read_root():
    return {"message": "Welcome to TJSP Criminal Records API. Use /search to check records."}

@app.get("/status")
def get_status():
    total = get_total_requests()
    return {
        "status": "online",
        "total_requests_processed": total
    }

@app.post("/search", response_model=SearchResponse)
async def search_records(request: SearchRequest, background_tasks: BackgroundTasks):
    document = request.document.strip()
    
    # Basic validation
    if not document:
        raise HTTPException(status_code=400, detail="Document is required")
    
    # Perform search
    result = await search_tjsp(document)
    
    # Format document for response
    formatted_doc = format_document(document)
    
    if "error" in result:
        # Log failure
        background_tasks.add_task(log_request, formatted_doc, "failed", 0, [], [])
        raise HTTPException(status_code=500, detail=f"Search failed: {result['error']}")
    
    count = result["count"]
    processes = result.get("details", []) # Scraper now returns dicts in 'details' key
    names = result.get("names", [])
    
    # Log success
    background_tasks.add_task(log_request, formatted_doc, "success", count, processes, names)
    
    return {
        "document": formatted_doc,
        "records_count": count,
        "processes": processes,
        "names": names,
        "status": "success"
    }

    return {
        "document": formatted_doc,
        "records_count": count,
        "processes": processes,
        "names": names,
        "status": "success"
    }

@app.post("/search-person")
async def search_person(request: SearchRequest):
    document = request.document.strip()
    
    if not document:
        raise HTTPException(status_code=400, detail="Document is required")
        
    # Format document
    formatted_doc = format_document(document)
    
    # Search Portal
    result = await search_portal_transparencia(formatted_doc)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=f"Search failed: {result['error']}")
        
    return {
        "document": formatted_doc,
        "data": result
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
