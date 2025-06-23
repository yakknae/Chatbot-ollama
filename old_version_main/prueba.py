from langchain_ollama import OllamaLLM
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import mysql.connector
import os
from dotenv import load_dotenv
import json

load_dotenv()

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
model = OllamaLLM(model="deepseek-r1")

# Prompt general para conversaciones
prompt = ChatPromptTemplate.from_messages([
    ("system", config.get("prompt", {}).get("message", "Eres un asistente virtual de un supermercado.")),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

chain = prompt | model

# Historial de mensajes
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = []
    return store[session_id]

with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# Función para conectar a la base de datos MySQL
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("host"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            database=os.getenv("database")
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

# Función para buscar productos por nombre
def get_product_info(product_name):
    if product_name.lower() in ["ninguno", "", "none"]:
        return None

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
        WHERE LOWER(p.nombre) LIKE %s OR LOWER(m.nombre) LIKE %s OR LOWER(c.nombre) LIKE %s
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
        WHERE LOWER(p.nombre) LIKE %s AND NOT LOWER(p.nombre) LIKE %s
        ORDER BY p.nombre ASC;"""

    first_word = product_name.strip().lower().split()[0] if product_name.strip().lower().split() else product_name.strip().lower()

    cursor.execute(QUERY_START, (f"{first_word}%", f"{first_word}%", f"{first_word}%"))
    start_results = cursor.fetchall()

    if start_results:
        cursor.close()
        connection.close()
        return start_results

    cursor.execute(QUERY_CONTAINS, (f"%{product_name.strip().lower()}%", f"{first_word}%"))
    contain_results = cursor.fetchall()

    cursor.close()
    connection.close()

    return contain_results or f"No se encontró ningún producto relacionado con '{product_name}'."

# Función para detectar producto desde IA
def detect_product_with_ai(user_input):
    prompt = f"""
Detecta el producto mencionado en la siguiente frase del usuario.

Reglas:
- Solo responde con el nombre del producto mencionado.
- No incluyas explicaciones ni justificaciones.
- Si no hay un producto claro, responde exactamente: "ninguno"
- La respuesta debe ser una sola palabra o frase corta.
- No uses comillas ni signos de puntuación extra.

Frase del usuario: "{user_input}"

Producto mencionado: 
"""

    detected_product = model.invoke(prompt).strip().lower()

    # Limpieza si el modelo devuelve cosas como "producto mencionado: galletitas"
    if ":" in detected_product:
        detected_product = detected_product.split(":")[-1].strip()

    detected_product = detected_product.strip("., ")

    if not detected_product or detected_product == "ninguno" or len(detected_product) < 2:
        return None

    return detected_product

# Función para obtener la respuesta del modelo
def get_response(user_input):
    user_input_lower = user_input.lower().strip()

    # 1. Verificar primero si coincide con alguna categoría del config.json
    for category, data in config.items():
        if category == "prompt":
            continue
        keywords = data.get("keywords", [])
        if any(keyword in user_input_lower for keyword in keywords):
            response = data.get("message", "Sin información disponible.")
            return response

    # 2. Usar IA para detectar producto
    detected_product = detect_product_with_ai(user_input)

    # 3. Validamos que el producto detectado sea válido
    if detected_product:
        print(f"Producto detectado por IA: {detected_product}")
        products = get_product_info(detected_product)
    else:
        print("Ningún producto detectado por IA.")
        products = None

    # 4. Si hay productos encontrados
    if isinstance(products, list):
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

        Basándote en la información proporcionada, enumera los tipos de productos disponibles, describe sus características principales y destaca su utilidad o ventajas. 
        Si solo hay uno, enfócate en él. Si hay varios, compáralos brevemente y resalta las diferencias clave.

        Proporciona una respuesta clara, amigable y útil para un cliente interesado en comprar este producto.

        Respuesta clara y amigable:
        """
        response = with_message_history.invoke(
            {"input": full_prompt},
            config={"configurable": {"session_id": "abc123"}}
        ).content
        return response

    elif isinstance(products, str):
        return products

    # 5. Última opción: Usar IA para responder de forma general
    response = with_message_history.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": "abc123"}}
    ).content
    return response

# Función principal para interactuar con el usuario
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

# Ejecutar la aplicación
if __name__ == "__main__":
    main()