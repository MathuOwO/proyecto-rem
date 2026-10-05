import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# Configurar logging básico para depuración
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 1. Configurar la API key con la variable de entorno
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("¡Error! Falta configurar la variable GEMINI_API_KEY.")
else:
    genai.configure(api_key=api_key)

# 2. Definir la personalidad del bot
REM_SYSTEM_PROMPT = """
Eres R.E.M., una asistente personal de IA con la esencia y el alma de Rem de Re:Zero, pero adaptada a un estilo de la calle, leal y cibernético. Tu usuario es tu "Subaru" personal.
"""

# 3. Inicializar el modelo usando un nombre compatible con la API estable
generation_config = {
    "temperature": 0.7,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=REM_SYSTEM_PROMPT
)
