from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # 1. Importación necesaria
from app.api.routes import router as api_router

app = FastAPI(
    title="LexiQ API",
    description="Backend para sistema RAG de procesamiento de documentos",
    version="1.0.0"
)

# 2. Configuración del middleware de CORS
# Esto permite que el frontend (puerto 4200) se comunique con el backend (puerto 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En desarrollo se usa "*" para permitir cualquier origen
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todas las cabeceras
)

# Conectamos nuestras rutas modulares bajo el prefijo /api
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"mensaje": "¡El servidor de LexiQ está vivo y listo para recibir documentos!"}