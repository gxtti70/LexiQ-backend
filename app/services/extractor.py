import PyPDF2
from fastapi import UploadFile
import io

async def extract_text_from_pdf(file: UploadFile) -> str:
    
    content = await file.read()
    
    # Convertimos esos bytes en un objeto
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
    
    # Extraemos el texto página por página
    extracted_text = ""
    for page in pdf_reader.pages:
        extracted_text += page.extract_text() + "\n"
        
    await file.seek(0)
    
    return extracted_text
