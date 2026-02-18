import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv() # Se conecta con el archivo .env
API_KEY = os.getenv("GENAI_API_KEY")
# Inicializar el cliente
client = genai.Client(api_key=API_KEY)
configuration = types.GenerateContentConfig(
    max_output_tokens=2048,
    system_instruction="""Eres un modelo que ayuda a los estudiantes a responder preguntas, la respuesta no debe superar 50 tokens"""
)
text = "Que es la inferencia en IA? "
response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=configuration,
    contents=text
)
print(response.text)