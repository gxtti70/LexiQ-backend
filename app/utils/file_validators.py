from fastapi import HTTPException

# Diccionario con las extensiones permitidas
ALLOWED_EXTENSIONS = {"pdf", "docx", "xlsx", "pptx"}

def validate_file_extension(filename: str) -> str:
    # Extraemos la extensión del nombre del archivo
    ext = filename.split(".")[-1].lower()
    
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Formato no soportado. Por favor sube PDF, Word, Excel o PowerPoint. Recibido: {ext}"
        )
    return ext