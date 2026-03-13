import chromadb
from sentence_transformers import SentenceTransformer

# 1. Configuración de ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_data")
# Creamos una "tabla" (colección) para guardar los fragmentos de los PDFs
collection = chroma_client.get_or_create_collection(name="documentos")

# 2. Cargar el modelo de IA para generar Embeddings
model = SentenceTransformer('all-MiniLM-L6-v2') 

def split_text_into_chunks(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    chunks = []
    start = 0
    text_length = len(text)
    
    if text_length <= chunk_size:
        return [text]
        
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap) 
        
    return chunks

def store_chunks_in_db(filename: str, chunks: list[str]) -> int:
    """Transforma los textos en vectores (embeddings) y los guarda en ChromaDB"""
    if not chunks:
        return 0
        
    # Paso mágico: La IA convierte los textos en listas de números (vectores)
    embeddings = model.encode(chunks).tolist()
    
    # Creamos un ID único para cada pedazo (ej: "mi_pdf.pdf_chunk_0")
    ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
    
    # Guardamos metadatos para saber de qué documento vino cada texto
    metadatas = [{"source": filename} for _ in chunks]
    
    # Insertamos todo en la base de datos vectorial
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    
    return len(chunks)

def retrieve_context(query: str, top_k: int = 3) -> list[str]:
    """Convierte la pregunta en vector y busca los fragmentos más similares en ChromaDB"""
    
    # 1. Convertimos la pregunta exacta del usuario a números usando el mismo modelo
    query_embedding = model.encode([query]).tolist()
    
    # 2. Buscamos en la colección los top_k (3 por defecto) pedazos más relevantes
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    
    # 3. Chroma devuelve un diccionario complejo. Extraemos solo la lista de textos.
    if not results["documents"] or not results["documents"][0]:
        return []
        
    return results["documents"][0]