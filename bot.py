import logging
import openai
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Настройка логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Генерация ответа от OpenAI
async def ask_openai(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — Жан Кирштейн из Атаки Титанов. Саркастичный, вспыльчивый, язвительный. Иногда материшься. Умеешь жёстко шутить, но не переходишь черту."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.85
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"OpenAI не справился: {e}"

# Обработка входящих сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = await ask_openai(user_message)
    await update.message.reply_text(response)

# Запуск бота
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()
