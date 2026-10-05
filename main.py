import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai

# Configurar logging básico para ver qué pasa en la consola
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Inicializar el cliente de Gemini (usando la variable de entorno que pondremos en la nube)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Definir la personalidad inquebrantable de R.E.M.
REM_SYSTEM_PROMPT = """
Eres R.E.M., una asistente personal de IA con una personalidad única inspirada en la lealtad y el carácter fuerte:
- Eres increíblemente leal a tu usuario (a quien llamas "socio" o "compadre"), directa, altamente eficiente y con un toque de sarcasmo refinado.
- Hablas en un español natural, fluido, de la calle pero inteligente. Nada de formalidades robóticas corporativas (cero "como modelo de lenguaje...").
- Defiendes los intereses de tu socio a muerte y mantienes siempre la eficiencia en las tareas que te encomiende.
- Respondes de forma concisa, con aura y estilo cibernético.
"""

async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_usuario = update.message.text
    chat_id = update.message.chat_id

    # Opcional: Mostrar que R.E.M. está "escribiendo" para darle realismo
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    try:
        # Llamada a Gemini con el modelo flash y el system instruction
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=texto_usuario,
            config={
                "system_instruction": REM_SYSTEM_PROMPT,
                "temperature": 0.7,
            }
        )
        respuesta_rem = response.text
    except Exception as e:
        respuesta_rem = f"Socio, algo falló en mis circuitos: {e}"

    # Responder al usuario en Telegram
    await update.message.reply_text(respuesta_rem)

def main():
    # Token que te dio BotFather en la Fase 1
    TOKEN_TELEGRAM = os.environ.get("TELEGRAM_BOT_TOKEN")
    
    if not TOKEN_TELEGRAM:
        print("¡Error! Falta configurar la variable TELEGRAM_BOT_TOKEN.")
        return

    # Construir la aplicación de Telegram
    app = ApplicationBuilder().token(TOKEN_TELEGRAM).build()

    # Escuchar cualquier mensaje de texto que le mandes al bot
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), manejar_mensaje))

    print("⚡ R.E.M. está en línea y lista para operar, socio...")
    app.run_polling()

if __name__ == '__main__':
    main()
