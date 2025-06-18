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

#Cargar querys de la carpeta querys
def load_query(filename):
    try:
        with open(filename,'r',encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo de consulta: {filename}")

#Instanciar las query
QUERY_START = load_query("querys/query_start.sql")
QUERY_CONTAINS = load_query("querys/query_contains.sql")
QUERY_BRAND = load_query("querys/query_brand.sql")
QUERY_SECTION = load_query("querys/query_section.sql")

def load_promps(filename):
    try:
        with open(filename,'r',encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"no se encontro el archivo de consulta {filename}")

#Instanciar los promps
PROMP_DETECT = load_promps("promps/promps_detect_product.txt")


# Configuración inicial del modelo Ollama
model = OllamaLLM(model="llama3.2")

# Crear una memoria para el historial de la conversación
memory = ConversationBufferMemory()

# Crear la cadena de conversación
conversation = ConversationChain(llm=model, memory=memory, verbose=True)

#Cargar querys de la carpeta querys
def load_query(filename):
    try:
        with open(filename,'r',encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo de consulta: {filename}")

#Instanciar las query
QUERY_START = load_query("querys/query_start.sql")
QUERY_CONTAINS = load_query("querys/query_contains.sql")
QUERY_BRAND = load_query("querys/query_brand.sql")
QUERY_SECTION = load_query("querys/query_section.sql")

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

    product_name_lower = product_name.strip().lower()
    words = product_name.split()
    first_word = words[0].strip() if words else product_name_lower

    # Búsqueda por coincidencia inicial
    cursor.execute(QUERY_START, (f"{first_word}%", f"%{first_word}%", f"%{first_word}%"))
    start_results = cursor.fetchall()

    if start_results:
        cursor.close()
        connection.close()
        return start_results

    # Búsqueda por coincidencia parcial
    cursor.execute(QUERY_CONTAINS, (f"%{product_name_lower}%", f"{product_name_lower}%"))
    contain_results = cursor.fetchall()

    cursor.close()
    connection.close()

    if contain_results:
        return contain_results

    return []

# Función para buscar marcas por nombre
def get_brand_info(brand_name):
    connection = connect_to_db()
    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)

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

    cursor.execute(QUERY_SECTION, (f"%{section_name}%",))
    sections = cursor.fetchall()

    cursor.close()
    connection.close()
    return sections

def detect_product_with_ai(user_input):
    # Prompt específico para pedirle al modelo que identifique SOLO el producto
    prompt = f"""
    Eres un asistente especializado en detectar productos o categorias mencionados en frases de compradores.
    Tu tarea es identificar el nombre del producto o categorias mencionado en la siguiente frase.

    Frase del usuario: "{user_input}"

    Producto mencionado (solo el nombre, sin texto adicional): 
    """

    try:
        # Pasamos el prompt completo al modelo
        detected_product = model.invoke(prompt).strip().lower()

        # Limpieza adicional si el modelo devuelve más texto del necesario
        if "producto detectado:" in detected_product:
            detected_product = detected_product.split("producto detectado:")[-1].strip().rstrip('.').strip()

        # Si el resultado es "ninguno", vacío o muy corto, retornamos None
        if not detected_product or detected_product == "ninguno" or len(detected_product) < 2:
            return None

        return detected_product

    except Exception as e:
        print(f"Error al detectar producto con IA: {e}")
        return None

# Función para obtener la respuesta del modelo
def get_response(user_input):
    detected_product = detect_product_with_ai(user_input)

    if detected_product:
        print(f"producto detectado: {detected_product}")
        products = get_product_info(detected_product)

        if isinstance(products, list) and len(products) > 0:
            context = "Información de productos encontrados:\n"
            for product in products:
                stock_status = "Disponible" if product["stock"] > 0 else "Agotado"
                context += (
                    f"- Nombre: {product['producto']}\n"
                    f"  Descripción: {product['descripcion'] or 'Sin descripción'}\n"
                    f"  Stock: {product['stock']} ({stock_status})\n"
                    f"  Marca: {product['marca'] or 'Sin marca'}\n"
                    f"  Categoría: {product['categoria'] or 'Sin categoría'}\n"
                    f"  Precio: {product['precio_venta']}\n"
                )

            full_prompt = f"{context}\nPregunta del usuario: {user_input}\nRespuesta:"
            response = conversation.invoke(full_prompt)
            conversation.memory.chat_memory.add_user_message(user_input)
            conversation.memory.chat_memory.add_ai_message(response)
            return response

        else:
            # No se encontraron productos reales
            conversation.memory.chat_memory.add_user_message(user_input)
            msg = f"No encontré productos relacionados con '{detected_product}' en este momento."
            conversation.memory.chat_memory.add_ai_message(msg)
            return msg

    # Si no se detectó producto, revisar config.json
    user_input_lower = user_input.lower()
    for category, data in config.items():
        if category == "prompt":
            continue

        keywords = data.get("keywords", [])
        if any(keyword in user_input_lower for keyword in keywords):
            response = data.get("message", "Sin información disponible.")
            conversation.memory.chat_memory.add_user_message(user_input)
            conversation.memory.chat_memory.add_ai_message(response)
            return response

    # Respuesta por defecto usando prompt genérico
    default_context = config.get("prompt", {}).get("message", "Eres un asistente virtual de un supermercado.")
    prompt = f"{default_context}\nPregunta del usuario: {user_input}\nRespuesta:"
    response = conversation.invoke(prompt)
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