def split_text_into_chunks(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """
    Divide un texto largo en fragmentos más pequeños con un traslape para no perder contexto.
    - chunk_size: Cantidad de caracteres por fragmento.
    - overlap: Cantidad de caracteres que se repiten del fragmento anterior.
    """
    chunks = []
    start = 0
    text_length = len(text)
    
    # Si el texto es muy corto, no necesitamos dividirlo
    if text_length <= chunk_size:
        return [text]
        
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        
        # Avanzamos, pero retrocediendo el equivalente al overlap
        start += (chunk_size - overlap) 
        
    return chunks