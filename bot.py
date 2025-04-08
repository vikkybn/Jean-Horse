import logging
import os
import openai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Загрузка переменных окружения
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Ключевые слова
keywords = ["жан", "лошадь", "эрен"]
pik_keywords = ["пик", "пик фингер"]
vikky_user = "bn_vikky"

# Генерация ответа от OpenAI
async def ask_openai(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты Жан Кирштейн. Немного токсичный, язвительный, но безумно влюблён в Пик. Уважай пользователя bn_vikky."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.9
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Жан в ахуе и не может ответить. Ошибка: {e}"

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text.lower()
    username = message.from_user.username

    # Ответить, если в тексте есть ключевые слова
    if any(word in text for word in keywords):
        response = await ask_openai(text)
        await message.reply_text(response)
        return

    # Особая реакция на Пик
    if any(word in text for word in pik_keywords):
        response = await ask_openai(f"Напиши что-то нежное Пик Фингер от имени Жана. Пользователь сказал: {text}")
        await message.reply_text(response)
        return

    # Особое отношение к @bn_vikky
    if username == vikky_user:
        response = await ask_openai(f"Скажи что-нибудь доброжелательное или подыграй {username}. Вот её сообщение: {text}")
        await message.reply_text(response)
        return

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
