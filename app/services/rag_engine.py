import chromadb
from sentence_transformers import SentenceTransformer

# Configuración de ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_data")
# Creamos una "tabla" para guardar los fragmentos de los PDFs
collection = chroma_client.get_or_create_collection(name="documentos")

# Se carga el modelo de Lexi
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
        
    embeddings = model.encode(chunks).tolist()
    
    ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
    
    # Guarda metadatos para saber de qué documento vino cada texto
    metadatas = [{"source": filename} for _ in chunks]
    
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    
    return len(chunks)

def retrieve_context(query: str, top_k: int = 3) -> list[str]:
    """Convierte la pregunta en vector y busca los fragmentos más similares en ChromaDB"""
    
    query_embedding = model.encode([query]).tolist()
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    
    if not results["documents"] or not results["documents"][0]:
        return []
        
    return results["documents"][0]
