from langchain_ollama import OllamaLLM
import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()



# Configuración inicial del modelo Ollama
model = OllamaLLM(model="llama3.2")


# Función para conectar a la base de datos MySQL
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("host"), # Cambia esto según tu configuración
            user=os.getenv("user"),      # Cambia esto según tu configuración
            password=os.getenv("password"),    # Cambia esto según tu configuración
            database=os.getenv("database")   # Nombre de tu base de datos
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

# Función para buscar un socio por DNI o email
def get_socio_info(identifier):
    connection = connect_to_db()
    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT 
            id_socio, nombre, apellido, dni, fecha_nacimiento, genero, email, telefono, direccion,
            id_plan, id_plan_social, estado, fecha_ingreso
        FROM socios
        WHERE dni = %s OR email = %s;
    """
    cursor.execute(query, (identifier, identifier))
    socio = cursor.fetchone()

    cursor.close()
    connection.close()
    return socio

# Función para formatear la información del socio
def format_socio_info(socio):
    if not socio:
        return "No se encontró información del socio."

    fecha_nacimiento = socio["fecha_nacimiento"].strftime("%d/%m/%Y") if socio["fecha_nacimiento"] else "No disponible"
    fecha_ingreso = socio["fecha_ingreso"].strftime("%d/%m/%Y") if socio["fecha_ingreso"] else "No disponible"

    info = (
        f"Información del Socio:\n"
        f"ID: {socio['id_socio']}\n"
        f"Nombre: {socio['nombre']} {socio['apellido']}\n"
        f"DNI: {socio['dni']}\n"
        f"Fecha de Nacimiento: {fecha_nacimiento}\n"
        f"Género: {socio['genero'] or 'No disponible'}\n"
        f"Email: {socio['email']}\n"
        f"Teléfono: {socio['telefono'] or 'No disponible'}\n"
        f"Dirección: {socio['direccion'] or 'No disponible'}\n"
        f"Plan ID: {socio['id_plan'] or 'No asignado'}\n"
        f"Plan Social ID: {socio['id_plan_social'] or 'No asignado'}\n"
        f"Estado: {socio['estado']}\n"
        f"Fecha de Ingreso: {fecha_ingreso}"
    )
    return info

# Función para obtener la respuesta del modelo
def get_response(user_input):
    user_input_lower = user_input.lower()

    # Detectar si el usuario está buscando información de un socio
    keywords = ["socio", "información", "datos", "plan", "ingreso"]
    for keyword in keywords:
        if keyword in user_input_lower:
            # Extraer el identificador (DNI o email) del mensaje del usuario
            identifier = user_input_lower.split()[-1] 
            socio = get_socio_info(identifier)

            # Si se encuentra información del socio, generar contexto para Ollama
            if socio:
                socio_info = format_socio_info(socio)
                context = f"Información del socio solicitado:\n{socio_info}"
                prompt = f"{context}\nPregunta del usuario: {user_input}\nRespuesta:"
                response = model.invoke(prompt)
                return response
            else:
                return "No se encontró información del socio solicitado."

    # Si no coincide con ninguna categoría, usa el modelo Ollama sin contexto
    context = "Eres un asistente virtual de una tienda de herramientas."
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