from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(
    title="LexiQ API",
    description="Backend para sistema RAG de procesamiento de documentos",
    version="1.0.0"
)

# Conectamos nuestras rutas modulares bajo el prefijo /api
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"mensaje": "¡El servidor de LexiQ está vivo y listo para recibir documentos!"}