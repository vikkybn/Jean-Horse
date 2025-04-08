
import logging
import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Настройки логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Получаем токены из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Ключевые слова
keywords = ["жан", "лошадь", "эрен"]
pik_keywords = ["пик", "пик фингер"]
vikky_user = "bn_vikky"

# Генерация текста через OpenAI
async def ask_openai(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты Жан Кирштейн. Немного дерзкий, немного токсичный, но харизматичный. Очень влюблён в Пик Фингер и уважаешь пользователя bn_vikky."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.9,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Жан в ахуе и не может ответить. Ошибка: {e}"

# Обработка входящих сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text.lower()
    username = message.from_user.username.lower() if message.from_user.username else ""

    if not text:
        return

    # Поведение при сообщениях от @bn_vikky
    if username == vikky_user:
        await message.reply_text("Для тебя — что угодно. Только скажи, @bn_vikky.")
        return

    # Поведение при упоминании Пик
    if any(word in text for word in pik_keywords):
        await message.reply_text("Ты сказала 'Пик'? Моя любовь, моя муза… Эх.")
        return

    # Поведение при ключевых словах
    if any(word in text for word in keywords):
        response = await ask_openai(text)
        await message.reply_text(response)
        return

    # Поведение при прямом упоминании
    if f"@{context.bot.username.lower()}" in text or message.reply_to_message and message.reply_to_message.from_user.username == context.bot.username:
        response = await ask_openai(text)
        await message.reply_text(response)

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
