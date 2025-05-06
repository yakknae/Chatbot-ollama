from langchain_ollama import OllamaLLM
import json

# Cargar configuración desde el archivo JSON
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Configuración inicial del modelo Ollama
model = OllamaLLM(model="llama3.2")

# Cargar el contexto desde el JSON
context = config["prompt"]

# Función para obtener la respuesta del modelo
def get_response(user_input):
    user_input_lower = user_input.lower()

    # Detectar si es una pregunta sobre una seccion
    for category_key in config:
        if category_key == "prompt":
            continue

        category = config[category_key]
        for keyword in category["keywords"]:
            if keyword in user_input_lower:
                return category["message"]
        
    prompt = f"{context}\nPregunta del usuario: {user_input}\nRespuesta:"
    response = model.invoke(prompt)
    return response

# Función principal para interactuar con el usuario
def main():
    print("¡Bienvenido al Asistente Virtual de la Tienda de Herramientas!")
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