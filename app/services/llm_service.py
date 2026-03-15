import os
from groq import Groq
from dotenv import load_dotenv

# Cargamos las variables ocultas del archivo .env
load_dotenv()

# Inicializamos el cliente. Automáticamente buscará la GROQ_API_KEY
client = Groq()

def generate_answer(question: str, context_chunks: list[str]) -> str:
    """Toma la pregunta y los pedazos de PDF, y redacta una respuesta humana"""
    
    # Unimos los pedazos de texto que encontraste en un solo gran bloque
    context = "\n\n---\n\n".join(context_chunks)
    
    # Le damos instrucciones estrictas a la IA
    system_prompt = f"""
    Eres LexiQ, un asistente experto y profesional analizando documentos. 
    Responde a la pregunta del usuario basándote ÚNICAMENTE en el contexto proporcionado abajo.
    Si la respuesta a la pregunta no se encuentra en el contexto, debes responder exactamente: 'No tengo suficiente información en el documento para responder a esta pregunta'.
    No inventes información.
    
    CONTEXTO EXTRAÍDO DEL DOCUMENTO:
    {context}
    """
    
    try:
        # Llamamos a Groq usando el modelo Llama 3 de Meta (súper rápido y eficiente)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": question,
                }
            ],
            model="llama-3.1-8b-instant", 
            temperature=0.2, # Temperatura baja para que sea analítico y no creativo/inventivo
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error de conexión con el cerebro LLM: {str(e)}"