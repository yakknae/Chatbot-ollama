from langchain_ollama import OllamaLLM
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
#model = OllamaLLM(model="llama3.2")
model = OllamaLLM(model="deepseek-r1:14b")

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
    query = """
        SELECT 
            p.id, p.nombre 'producto', p.descripcion, p.precio_costo, p.precio_venta, p.stock, m.nombre 'marca', c.nombre 'categoria'
        FROM productos p INNER JOIN marcas m ON p.marca_id = m.id INNER JOIN categorias c ON p.categoria_id = c.id
        WHERE LOWER(p.nombre) LIKE %s OR LOWER(m.nombre) LIKE %s OR LOWER(c.nombre) LIKE %s 
        ;
    """
    # Convertir el nombre del producto a minúsculas para mejorar la coincidencia
    
    product_name_lower = product_name.lower()
    #print(query, (f"%{product_name_lower}%", f"%{product_name_lower}%", f"%{product_name_lower}%"))
    cursor.execute(query, (f"%{product_name_lower}%", f"%{product_name_lower}%", f"%{product_name_lower}%"))
    products = cursor.fetchall()

    cursor.close()
    connection.close()
    

    if not products:
        return f"No se encontró ningún producto con el nombre '{product_name}'."

    return products

# Función para buscar marcas por nombre
def get_brand_info(brand_name):
    connection = connect_to_db()
    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT 
            id_marca, nombre
        FROM marca
        WHERE nombre LIKE %s;
    """
    cursor.execute(query, (f"%{brand_name}%",))
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
    query = """
        SELECT 
            id_seccion, nombre
        FROM seccion
        WHERE nombre LIKE %s;
    """
    cursor.execute(query, (f"%{section_name}%",))
    sections = cursor.fetchall()

    cursor.close()
    connection.close()
    return sections


# Función para obtener la respuesta del modelo
def get_response(user_input):
    user_input_lower = user_input.lower()
    print("****GET RESPONSE****")
    # Verificar si la pregunta coincide con alguna categoría del config.json
    for category, data in config.items():
        if category == "prompt":  # Ignorar la clave "prompt"
            continue

        keywords = data.get("keywords", [])
        if any(keyword in user_input_lower for keyword in keywords):
            return data.get("message", "Sin información disponible.")
 
   
    # Detectar si el usuario está buscando información de productos
    product_keywords = ["producto", "productos", "artículo", "articulo","articulos"]
    print("Usuario puso: " + user_input_lower)
    if any(keyword in user_input_lower for keyword in product_keywords):
        print("detectada la keyword")
        # Extraer el nombre del producto (todo después de la palabra clave)
        product_name = " ".join(user_input_lower.split()[1:])
        if not product_name.strip():
            return "Por favor, especifique el nombre del producto que desea buscar."

        products = get_product_info(product_name)

        if isinstance(products, str):  # Si no se encontraron productos
            return products

        # Construir el contexto para Ollama
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

        # Generar la respuesta usando Ollama
        prompt = f"{context}\nPregunta del usuario: {user_input}\nRespuesta:"
        response = model.invoke(prompt)
        return response

    # Respuesta predeterminada si no se detecta ninguna categoría
    context = config.get("prompt", {}).get("message", "Eres un asistente virtual de un supermercado.")
    prompt = f"{context}\nPregunta del usuario: {user_input}\nRespuesta:"
    response = model.invoke(prompt)
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