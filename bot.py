import logging
import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Ключевые слова
keywords = ["жан", "лошадь", "эрен"]
pik_keywords = ["пик", "пик фингер"]
vikky_user = "bn_vikky"

# OpenAI ответ
async def ask_openai(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты Жан Кирштейн. Немного грубый, язвительный, влюблён в Пик Фингер. К bn_vikky — тепло, как к подруге или возлюбленной."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=120,
            temperature=0.9,
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Жан в ахуе и не может ответить. Ошибка: {e}"

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text.lower()
    sender_username = message.from_user.username

    is_reply = message.reply_to_message and message.reply_to_message.from_user.username == context.bot.username
    is_mention = f"@{context.bot.username.lower()}" in text
    has_keyword = any(word in text for word in keywords)

    if not (is_reply or is_mention or has_keyword):
        return

    if any(word in text for word in pik_keywords):
        await message.reply_text("Пик... Она — воплощение грации и ума. Кто сможет устоять?")
        return

    if sender_username == vikky_user:
        text = f"Сообщение от bn_vikky: {text}"

    response = await ask_openai(text)
    await message.reply_text(response)

# Запуск
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
