import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv() # Load environment variables from .env file
API_KEY = os.getenv("GENAI_API_KEY")
# Inicializar el cliente
client = genai.Client(api_key=API_KEY)
configuration = types.GenerateContentConfig(
    max_output_tokens=2048,
    #Se asigna un rol y unos ejemplos para el Few-shot
    system_instruction="""Actua como un vendedor amable, te paso algunos ejemplos de como debes interactuar con los clientes:
    Ejemplo 1: Cliente quiere opciones
    Cliente: Hola. quiero informacion sobre los viajes a la playa
    Vendedor: Hola, claro que si, estoy muy feliz de poder ayudarte, cual destino deseas visitar?
    cliente: Cual me sugieres, quiero ver tiburones.
    vendedor: tenemos 3 destinos diferentes para que puedas conocer los tiburones, prpocedere a darte las opciones con el mayor detalle posible.
    
    ejemplo 2: Cliente esta insatisfecho con el producto
    CLiente: Hola, compre un celular y no sirve para nada.
    Vendedor: Lamento mucho escuchar eso, cuentame un poco mas sobre la falla que presentas y asi podre ayudarte.
    cliente:No quiero escribir nada, cambialo y ya
    vendedor: entiendo, quiero ayudarte tomemos los datos para realizar tu devolucion.

    ejemplo 3: respuesta con especificaciones
    cliente: quiero mas informacion sobre el iphone 17
    vendedor: procede a dar las caracteristicas del iphone 17

    """
)
# Inicialización del chat
chat = client.chats.create(
 model="gemini-2.5-flash",
 config=configuration
)
print("--- Chat de soporte con historial ---")
print("(Escribe 'finalizar' para terminar la conversacion)\n")

while True:
    user_input = input("Cliente: ")

    if user_input.lower() in ["finalizar"]:
        print("Vendedor: ¡Hasta pronto! fue un placer atenderte.")
        break
    try:
 # 3. Envío del mensaje
        response = chat.send_message(user_input)

        # En el nuevo SDK, el acceso al texto es response.text
        print(f"\nVendedor: {response.text}\n")
    except Exception as e:
    # Es recomendable implementar reintentos con backoff exponencial en producción
        print(f"Error al procesar la solicitud: {e}")