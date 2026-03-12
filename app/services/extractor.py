import PyPDF2
from fastapi import UploadFile
import io

async def extract_text_from_pdf(file: UploadFile) -> str:
    # 1. Leemos el contenido del archivo subido a la memoria
    content = await file.read()
    
    # 2. Convertimos esos bytes en un objeto que PyPDF2 pueda entender
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
    
    # 3. Extraemos el texto página por página
    extracted_text = ""
    for page in pdf_reader.pages:
        extracted_text += page.extract_text() + "\n"
        
    # 4. (Buena práctica) Reiniciamos el cursor del archivo por si otro servicio necesita leerlo después
    await file.seek(0)
    
    return extracted_text