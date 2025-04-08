import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI

# Инициализация клиента OpenAI
client = OpenAI()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токены из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ключевые слова и пользователи
keywords = ["жан", "лошадь", "эрен"]
pik_keywords = ["пик", "пик фингер"]
vikky_user = "bn_vikky"

# Генерация текста через OpenAI
async def ask_openai(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — Жан Кирштейн из Атаки Титанов. Отвечай дерзко, с характером, грубо, но с особой теплотой к Пик Фингер и bn_vikky."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.9
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Жан в ахуе и не может ответить. Ошибка: {str(e)}"

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    text = message.text.lower() if message.text else ""
    username = message.from_user.username.lower() if message.from_user.username else ""
    is_reply = message.reply_to_message and message.reply_to_message.from_user.username == context.bot.username
    is_mention = f"@{context.bot.username.lower()}" in text

    if any(kw in text for kw in keywords) or is_reply or is_mention:
        prompt = text

        # Особая реакция на Пик
        if any(kw in text for kw in pik_keywords):
            prompt = f"Ответь с любовью, будто ты влюблен в Пик. {text}"

        # Особая реакция на Викки
        if username == vikky_user:
            prompt = f"Ответь с особой теплотой и уважением, ведь это Викки. {text}"

        response = await ask_openai(prompt)
        await message.reply_text(response)

# Основной запуск
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
