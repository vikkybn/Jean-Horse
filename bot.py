import logging
import random
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

TOKEN = "8049315123:AAEPZteF97DH2IMmdGId7o0RslLxXJnbMJ0"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

phrases = [
    "Ты опять? У меня уже нервный тик от ваших рож.",
    "Эрен, сука, ты снова решил сдохнуть геройски?! ХВАТИТ!",
    "Райнер? Шкаф на ножках. Говорит медленно, думает ещё медленнее.",
    "Если меня ещё раз разбудят — я кого-нибудь убью. Начну с тебя.",
    "Ты выглядишь, как титан после диареи.",
    "Я не псих, я просто служу в разведкорпусе. Тут все е**нутые.",
    "Микаса снова спасла задницу Эрена? Да за что ей это наказание?",
    "Если бы тупость была болезнью — ты бы уже не выжил.",
    "Опять проблемы? Я что, лицо ответственности?",
    "Да пошёл ты. Вежливо. Почти.",
    "Ты думаешь, у меня хорошее настроение? У меня просто морда такая.",
    "Пошли нахрен, у меня обед.",
    "Чего тебе, новобранец? Умнее стал? Нет? Тогда отвали.",
    "Леви опять молчит. Значит, кто-то умрёт.",
    "Меня бесит всё. Особенно ты.",
    "Только попробуй упомянуть титанов — я сблевану.",
    "Я Жан Кирштейн, мать вашу. Уважайте или катитесь.",
    "Если Райнер — твой кумир, то ты безнадёжен.",
    "Армин что-то придумал — ну, держитесь.",
    "Разведкорпус — где каждый день на грани инфаркта.",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Жан Кирштейн. Лучше бы ты не писал, но раз уж начал...")

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(phrases))

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))
    app.add_handler(MessageHandler(filters.ALL & filters.Entity("mention"), respond))
    app.add_handler(MessageHandler(filters.StatusUpdate.ALL, respond))
    app.run_polling()

if __name__ == "__main__":
    main()
