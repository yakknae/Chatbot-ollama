#commit de prueba JORGE
#commit de prueba JORGE 2
from langchain_ollama import OllamaLLM
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import mysql.connector
#import os
#from dotenv import load_dotenv
import json
import re

#load_dotenv()

# Cargar el archivo config.json
def load_config():
    try:
        with open("config.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: El archivo config.json no fue encontrado.")
        return None
    except json.JSONDecodeError:
        print("Error: El archivo config.json no es válido.")
        return None

# Cargar la configuración al inicio del programa
config = load_config()
if not config:
    exit("No se pudo cargar la configuración. Terminando el programa.")

# Configuración inicial del modelo Ollama
model = OllamaLLM(model="gemma3n:e4b")

# Prompt con historial
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente útil."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Cadena final
chain = prompt | model

# Historial en memoria
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# Función para conectar a la base de datos MySQL con valores fijos
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="0.tcp.sa.ngrok.io",    # poner acá tu host ngrok
            port=10257,                  # y tu puerto ngrok
            user="root",
            password="f289t",
            database="pp3_proyecto"
        )

        if connection.is_connected():
            print("Conexión exitosa a la base de datos.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

# (el resto del código igual, sin cambios)

def get_product_info(product_name):
    connection = connect_to_db()
    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)
    QUERY_START = """SELECT 
    p.id, 
    p.nombre AS producto, 
    p.descripcion, 
    p.precio_costo, 
    p.precio_venta, 
    p.stock, 
    m.nombre AS marca, 
    c.nombre AS categoria
    FROM productos p 
    INNER JOIN marcas m ON p.marca_id = m.id 
    INNER JOIN categorias c ON p.categoria_id = c.id
    WHERE LOWER(p.nombre) LIKE %s or LOWER(m.nombre) LIKE %s or LOWER(c.nombre) LIKE %s
    ORDER BY p.nombre ASC; """

    QUERY_CONTAINS = """SELECT 
    p.id, 
    p.nombre AS producto, 
    p.descripcion, 
    p.precio_costo, 
    p.precio_venta, 
    p.stock, 
    m.nombre AS marca, 
    c.nombre AS categoria
    FROM productos p 
    INNER JOIN marcas m ON p.marca_id = m.id 
    INNER JOIN categorias c ON p.categoria_id = c.id
    WHERE LOWER(p.nombre) LIKE %s
    AND NOT LOWER(p.nombre) LIKE %s
    ORDER BY p.nombre ASC;"""

    product_name_lower = product_name.strip().lower()
    words = product_name.strip().lower().split()
    first_word = words[0] if words else product_name_lower

    cursor.execute(QUERY_START, (f"{first_word}%", f"{first_word}%", f"{first_word}%"))
    start_results = cursor.fetchall()

    if start_results:
        cursor.close()
        connection.close()
        return start_results

    cursor.execute(QUERY_CONTAINS, (f"%{product_name_lower}%", f"{product_name_lower}%"))
    contain_results = cursor.fetchall()

    cursor.close()
    connection.close()

    if contain_results:
        return contain_results

    return f"No se encontró ningún producto relacionado con '{product_name}'."

def detect_product_with_ai(user_input):
    with open("prompts/prompt_input.txt", "r", encoding="utf-8") as file:
        prompt = file.read()
    
    prompt += f"""

Frase del usuario: "{user_input}"

Producto mencionado: 
"""
    detected_product = model.invoke(prompt).strip().lower()
    detected_product = re.sub(r"<think>.*?</think>", "", detected_product, flags=re.DOTALL | re.IGNORECASE).strip()

    if "producto mencionado" in detected_product:
        detected_product = detected_product.split(":")[-1].strip().rstrip(".").strip()

    detected_product = detected_product.rstrip(".")

    if not detected_product or detected_product == "ninguno" or len(detected_product) < 2:
        return None

    return detected_product

def get_response(user_input):
    user_input_lower = user_input.lower().strip()

    for category, data in config.items():
        if category == "prompt":
            continue
        keywords = data.get("keywords", [])
        if any(keyword in user_input_lower for keyword in keywords):
            response = data.get("message", "Sin información disponible.")
            return response

    detected_product = detect_product_with_ai(user_input)

    if detected_product:
        print(f"Producto detectado por IA: {detected_product}")
        products = get_product_info(detected_product)
    else:
        print("Ningún producto detectado por IA.")
        products = None

    if products and isinstance(products, list):
        context = "Tenemos estos tipos de productos disponibles:\n"
        for product in products:
            stock_status = "Disponible" if product.get("stock", 0) > 0 else "Agotado"
            name = product.get('producto', 'Producto sin nombre')
            description = product.get('descripcion', 'Sin descripción')
            brand = product.get('marca', 'Marca desconocida')
            price = product.get('precio_venta', 'Precio no disponible')
            category = product.get('categoria', 'Categoría desconocida')

            context += (
                f"- **{name}**\n"
                f"  - Descripción: {description}\n"
                f"  - Marca: {brand}\n"
                f"  - Categoría: {category}\n"
                f"  - Precio: ${price}\n"
                f"  - Stock: {product.get('stock', 0)} unidades ({stock_status})\n\n"
            )

        full_prompt = f"""
        {context}

        El usuario pregunta: "{user_input}"

        Solo muestra los productos relacionados con esa búsqueda, sin añadir opiniones ni descripciones extra. Muestra únicamente lo que tenemos disponible.

        Respuesta clara y amigable:
        """
        response = with_message_history.invoke(
            {"input": full_prompt},
            config={"configurable": {"session_id": "abc123"}}
        )
        return response

    elif isinstance(products, str):
        return products

    with open("prompts/prompt_output.txt", "r", encoding="utf-8") as fileOut:
        promptOutput = fileOut.read()
    
    default_context = config.get("prompt", {}).get("message", promptOutput)
    prompt = f"{default_context}\nPregunta del usuario: {user_input}\nRespuesta:"
    response = with_message_history.invoke(
        {"input": prompt},
        config={"configurable": {"session_id": "abc123"}}
    )
    return response

def main():
    print("¡Bienvenido al Asistente Virtual!")
    print("Escribe 'salir' para terminar la conversación.\n")
    
    while True:
        user_input = input("Tú: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("Bot: ¡Gracias por visitarnos! Hasta luego.")
            break

        response = get_response(user_input)
        print(f"Bot: {response}\n")

if __name__ == "__main__":
    main()
