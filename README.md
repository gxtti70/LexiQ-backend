# LexiQ: Asistente Inteligente de Documentos (RAG)

LexiQ es una aplicación Full-Stack impulsada por Inteligencia Artificial que permite a los usuarios subir documentos PDF y "chatear" con ellos. Utiliza la arquitectura RAG (Retrieval-Augmented Generation) para extraer respuestas precisas basadas únicamente en el contexto del documento proporcionado.

## Características Principales
* **Procesamiento de Documentos:** Sube archivos PDF para extracción automática de texto.
* **Búsqueda Semántica:** Fragmentación inteligente (chunking) y vectorización de documentos.
* **Chat Interactivo:** Interfaz fluida y moderna para conversar con la IA en tiempo real.
* **Cero Alucinaciones:** Las respuestas están estrictamente fundamentadas en el contexto del PDF subido.

## 🛠️ Tecnologías Utilizadas

**Frontend:**
* Angular (con Signals para manejo de estado reactivo)
* Tailwind CSS (diseño responsivo y UI/UX moderno)
* TypeScript

**Backend & IA:**
* Python & FastAPI (API REST ultrarrápida)
* ChromaDB (Base de datos vectorial local)
* LangChain / LlamaIndex (Orquestación RAG)
* Groq API (Modelo LLM ultra-rápido: `llama-3.1-8b-instant`)

## Arquitectura del Sistema
1. **Ingesta:** El PDF se procesa, se divide en fragmentos (*chunks*) y se convierte en vectores (Embeddings).
2. **Almacenamiento:** Los vectores se guardan en ChromaDB.
3. **Recuperación (Retrieval):** Al hacer una pregunta, el sistema busca los fragmentos de texto más relevantes.
4. **Generación:** El modelo Llama 3.1 de Groq redacta una respuesta humana utilizando solo el contexto recuperado.

## Instalación y Uso Local

### Configuración del Backend (Python/FastAPI)
1. Clona el repositorio.
2. Crea un entorno virtual: `python -m venv venv`
3. Activa el entorno y ejecuta: `pip install -r requirements.txt`
4. Crea un archivo `.env` en la raíz y añade tu API Key de Groq: `GROQ_API_KEY=tu_clave_aqui`
5. Inicia el servidor: `uvicorn main:app --reload` (Correrá en `localhost:8000`)

### Configuración del Frontend (Angular)
1. Ve a la carpeta del frontend y abre una terminal.
2. Instala las dependencias: `npm install`
3. Inicia el servidor de desarrollo: `ng serve`
4. Abre tu navegador en `http://localhost:4200`
