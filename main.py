from langchain_ollama import OllamaLLM
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
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
model = OllamaLLM(model="llama3.2")

# Crear una memoria para el historial de la conversación
memory = ConversationBufferMemory()

# Crear la cadena de conversación
conversation = ConversationChain(llm=model, memory=memory, verbose=True)

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
    connection = connect_to_db()
    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)
    # Consulta para productos que COMIENZAN con el nombre dado
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
    WHERE LOWER(p.nombre) LIKE %s
    ORDER BY p.nombre ASC; """

    # Consulta para productos que CONTIENEN el nombre dado

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
    if words:
        first_word = words[0]
    else:
        first_word = product_name.strip().lower()

    # Usar la consulta externa
    cursor.execute(QUERY_START, (f"{first_word}%",))
    start_results = cursor.fetchall()

    if start_results:
        cursor.close()
        connection.close()
        return start_results

    # Si no hay coincidencias al inicio, buscar que contenga el término
    cursor.execute(QUERY_CONTAINS, (f"%{product_name_lower}%", f"{product_name_lower}%"))
    contain_results = cursor.fetchall()

    cursor.close()
    connection.close()

    if contain_results:
        return contain_results

    return f"No se encontró ningún producto relacionado con '{product_name}'."

# Función para buscar marcas por nombre
def get_brand_info(brand_name):
    connection = connect_to_db()
    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)
    QUERY_BRAND = """
    SELECT 
    id, nombre
    FROM marcas
    WHERE nombre LIKE %s;"""

    cursor.execute(QUERY_BRAND, (f"%{brand_name}%",))
    brands = cursor.fetchall()

    cursor.close()
    connection.close()
    return brands

# Función para buscar secciones por nombre
def get_section_info(section_name):
    connection = connect_to_db()
    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)
    QUERY_SECTION = """SELECT 
    id, nombre
    FROM categorias
    WHERE nombre LIKE %s;
    """
    cursor.execute(QUERY_SECTION, (f"%{section_name}%",))
    sections = cursor.fetchall()

    cursor.close()
    connection.close()
    return sections

def detect_product_with_ai(user_input):
    prompt = f"""
Eres un asistente especializado en detectar productos mencionados en frases de compradores.
Tu tarea es identificar claramente el nombre del producto mencionado en la frase del usuario.
Solo responde con el nombre del producto. Si no hay un producto claro, responde solo con "ninguno".

Frase del usuario: "{user_input}"
Producto mencionado (solo el nombre): 
"""
    detected_product = model.invoke(prompt).strip().lower()

    # Limpieza si el modelo devuelve cosas como "producto mencionado: galletas"
    if "producto mencionado" in detected_product:
        detected_product = detected_product.split(":")[-1].strip().rstrip(".").strip()

    # Si termina con punto, lo eliminamos
    detected_product = detected_product.rstrip(".")

    # Si el resultado es vacío, "ninguno" o muy corto, devolvemos None
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
            conversation.memory.chat_memory.add_user_message(user_input)
            conversation.memory.chat_memory.add_ai_message(response)
            return response

    # 2. Solo si NO hay coincidencia en config.json, usar IA para detectar producto
    detected_product = detect_product_with_ai(user_input)

    if detected_product:
        print(f"Producto detectado por IA: {detected_product}")
        products = get_product_info(detected_product)
    else:
        print("Ningún producto detectado por IA.")
        products = None

    # 3. Si hay productos encontrados
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

        # Prompt personalizado para hacerlo más específico
        full_prompt = f"""
        {context}

        El usuario pregunta: "{user_input}"

        Basándote en la información proporcionada, enumera los tipos de productos disponibles, describe sus características principales y destaca su utilidad o ventajas. 
        Si solo hay uno, enfócate en él. Si hay varios, compáralos brevemente y resalta las diferencias clave.

        Proporciona una respuesta clara, amigable y útil para un cliente interesado en comprar este producto.

        Respuesta clara y amigable:
        """
        response = conversation.invoke({"input": full_prompt})["response"]
        conversation.memory.chat_memory.add_user_message(user_input)
        conversation.memory.chat_memory.add_ai_message(response)
        return response

    elif isinstance(products, str):
        conversation.memory.chat_memory.add_user_message(user_input)
        conversation.memory.chat_memory.add_ai_message(products)
        return products

    # 4. Respuesta predeterminada
    default_context = config.get("prompt", {}).get("message", "Eres un asistente virtual de un supermercado.")
    prompt = f"{default_context}\nPregunta del usuario: {user_input}\nRespuesta:"
    response = conversation.invoke({"input": prompt})["response"]
    conversation.memory.chat_memory.add_user_message(user_input)
    conversation.memory.chat_memory.add_ai_message(response)
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