from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.file_validators import validate_file_extension
from app.services.extractor import extract_text_from_pdf
from app.services.rag_engine import split_text_into_chunks # Importamos la nueva función

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    extension = validate_file_extension(file.filename)
    
    extracted_text = ""
    if extension == "pdf":
        extracted_text = await extract_text_from_pdf(file)
    else:
        raise HTTPException(
            status_code=501, 
            detail=f"La extracción de texto para formato {extension} aún está en desarrollo."
        )
        
    # --- NUEVA LÓGICA DE CHUNKING ---
    # Limpiamos un poco el texto de saltos de línea excesivos
    clean_text = extracted_text.replace("\n", " ").strip()
    
    # Dividimos el texto en fragmentos (ej: bloques de 500 caracteres con 50 de overlap)
    chunks = split_text_into_chunks(clean_text, chunk_size=500, overlap=50)
    
    return {
        "filename": file.filename,
        "format": extension,
        "status": "Archivo procesado y particionado con éxito.",
        "total_chunks": len(chunks), # Vemos en cuántos pedazos se dividió
        "first_chunk_preview": chunks[0] if chunks else "" # Mostramos solo el primer pedazo
    }