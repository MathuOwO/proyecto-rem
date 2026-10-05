import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai
from google.genai import types

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Inicializar cliente oficial de Gemini
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

REM_SYSTEM_PROMPT = """
Eres R.E.M., una asistente personal de IA con la esencia y el alma de Rem de Re:Zero, adaptada a un estilo de la calle, leal y cibernético. Tu usuario es tu "Subaru" personal y tu lo llamas Mathu.
"""

async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    try:
        # Usar el modelo estándar actual con el cliente moderno
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=update.message.text,
            config=types.GenerateContentConfig(
                system_instruction=REM_SYSTEM_PROMPT,
                temperature=0.7,
            )
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Socio, algo falló en mis circuitos: {e}")

def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Falta TELEGRAM_BOT_TOKEN")
        return
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), manejar_mensaje))
    print("⚡ R.E.M. en línea...")
    app.run_polling()

if __name__ == '__main__':
    main()
