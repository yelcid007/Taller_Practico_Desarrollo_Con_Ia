import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv() # Se conecta con el archivo .env
API_KEY = os.getenv("GENAI_API_KEY")
# Inicializar el cliente
client = genai.Client(api_key=API_KEY)
# Función para procesar el artículo según la tarea
def procesar_articulo(texto, tarea):
    # Definir la system_instruction como si fuera un "Editor Editorial de prestigio"
    system_instruction = "Eres un Editor Editorial de prestigio, capaz de procesar artículos de manera profesional."

    # Configuración general para la generación de contenido
    configuration = types.GenerateContentConfig(
        max_output_tokens=2480,  # Ajusta el límite según sea necesario
        system_instruction=system_instruction
    )
    
    # Definir el tipo de tarea y el texto procesado
    if tarea == "resumir":
        # Resumen ejecutivo
        task_instruction = "Por favor, resume este artículo de manera ejecutiva, manteniendo los puntos clave."
    elif tarea == "profesionalizar":
        # Hacer el texto más formal y técnico
        task_instruction = "Por favor, edita este artículo para que suene formal, técnico y profesional."
    else:
        return "Tarea no reconocida. Las tareas disponibles son: 'resumir' o 'profesionalizar'."

    # Incluir el texto original y la tarea en la consulta
    prompt = f"{task_instruction}\n\nTexto original: {texto}"

    # Realizar la consulta al modelo
    response = client.models.generate_content(
        model="gemini-2.5-flash",  # Modelo adecuado
        config=configuration,
        contents=prompt
    )

    # Procesar la respuesta del modelo
    try:
        result = response.candidates[0].content.parts[0].text  # Accede al contenido generado
        return result
    except (AttributeError, IndexError) as e:
        return f"Error al procesar la respuesta del modelo: {str(e)}"
        result = response.json()
        return result.get('answer', 'No se pudo obtener respuesta')
    else:
        return f"Error al procesar la solicitud: {response.status_code} - {response.text}"

# Función principal
def main():
    # Solicitar el texto del usuario
    texto = input("Escribe el texto que deseas procesar: ")

    # Solicitar la tarea a realizar (resumir o profesionalizar)
    tarea = input("¿Qué tarea deseas realizar? (resumir/profesionalizar): ").lower()

    # Llamar a la función procesar_articulo
    resultado = procesar_articulo(texto, tarea)

    # Imprimir el resultado
    print("\nResultado:")
    print(resultado)

# Ejecutar la función principal
if __name__ == "__main__":
    main()