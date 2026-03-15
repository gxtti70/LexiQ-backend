from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.file_validators import validate_file_extension
from app.services.extractor import extract_text_from_pdf
from app.services.rag_engine import split_text_into_chunks, store_chunks_in_db, retrieve_context
from app.models.schemas import QuestionRequest
from app.services.llm_service import generate_answer

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    extension = validate_file_extension(file.filename)
    
    extracted_text = ""
    if extension == "pdf":
        extracted_text = await extract_text_from_pdf(file)
    else:
        raise HTTPException(status_code=501, detail=f"Extracción para {extension} en desarrollo.")
        
    clean_text = extracted_text.replace("\n", " ").strip()
    
    # 1. Particionamos el texto
    chunks = split_text_into_chunks(clean_text, chunk_size=500, overlap=50)
    
    # 2. Vectorizamos y guardamos en la base de datos
    chunks_guardados = store_chunks_in_db(file.filename, chunks)
    
    return {
        "filename": file.filename,
        "format": extension,
        "status": "¡Éxito! Archivo procesado, vectorizado y almacenado en ChromaDB.",
        "chunks_almacenados": chunks_guardados
    }
@router.post("/ask")
async def ask_question(request: QuestionRequest):

    context_chunks = retrieve_context(request.question)
    
    if not context_chunks:
        return {
            "question": request.question,
            "answer": "No encontré información en los documentos para responder a esta pregunta.",
            "retrieved_context": []
        }
        
    #  Generar la respuesta humana usando el servicio LLM
    try:
        respuesta_ia = generate_answer(request.question, context_chunks)
    except Exception as e:
        # Por si la IA falla 
        respuesta_ia = f"Error al generar respuesta: {str(e)}"
    
    return {
        "question": request.question,
        "answer": respuesta_ia,  
        "retrieved_context": context_chunks,
        "status": "Éxito: Respuesta generada por LLM."
    }
