from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from informacion_negocio import info

# Crear modelo
model = OllamaLLM(model="llama3")

# Crear prompt y cadena
template = """
Información del negocio:
{info}

Pregunta:
{question}

Respuesta:
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Contexto global
context = ""

# App de FastAPI
app = FastAPI()

# Modelo de datos para recibir las preguntas
class Question(BaseModel):
    question: str

# Función para filtrar preguntas fuera de tema
def es_pregunta_relevante(pregunta):
    pregunta = pregunta.lower()

    temas_permitidos = [
        "laptop", "teléfono", "móvil", "iphone", "samsung", "xiaomi", "motorola", 
        "accesorio", "cargador", "auricular", "funda",
        "asesoramiento", "soporte técnico", "envío", "envíos", "envío gratuito",
        "ubicación", "dirección", "calle ficticia", "ciudad techno",
        "horario", "horarios", "atención", "hora de atención",
        "teléfono", "correo", "email", "contacto", "página web", "red social", "facebook", "instagram",
        "oferta", "descuento", "promoción",
        "devolución", "reembolso", "cambio de producto",
        "política de devoluciones", "calidad", "satisfacción",
    ]

    return any(tema in pregunta for tema in temas_permitidos)


# Endpoint para hacer preguntas
@app.post("/chat/")
async def chat_endpoint(q: Question):
    global context

    question = q.question

    if not es_pregunta_relevante(question):
        return {"bot": "Solo puedo responder preguntas relacionadas con la empresa y sus productos."}

    result = chain.invoke({
        "info": info,
        "context": context,
        "question": question
    })

    answer = result.content if hasattr(result, "content") else result
    context += f"\n\nPregunta: {question}\nRespuesta: {answer}"

    return {"bot": answer}
