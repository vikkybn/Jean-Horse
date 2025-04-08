import logging
import random
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, ContextTypes,
    CommandHandler, MessageHandler, filters,
    CallbackContext
)


TOKEN = "8049315123:AAEPZteF97DH2IMmdGId7o0RslLxXJnbMJ0"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

phrases = [
    "Когда вижу @AlcoColt_bot — хочется дезертировать.",
    "@AlcoColt_bot? Бухает и тупит. Как обычно.",
    "Если Кольт — твой кумир, иди переосмысли жизнь.",
    "Кто-то написал «титан»? Где мой прощальный напиток?",
    "Ты серьёзно сказал «атака»? Ты что, Эрен-стайл решил пойти?",
    "Я Жан Кирштейн, мать вашу. Уважайте или катитесь.", 
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
    "О, здравствуйте, опять вы, дебилы.",
    "Эрен, сука, ты опять решил всё взорвать, да?!",
    "Если я ещё раз увижу Райнера, я его ударю. Просто потому что могу.",
    "Ты кто такой вообще, командир понтов?",
    "Микаса опять всех спасла? Ну, неудивительно.",
    "Райнер — шкаф без мозга. Конец цитаты.",
    "Кольт? А, тот алкаш из штаба? Как он там?",
    "Леви смотрит на тебя, как на грязь. Я тоже, если что.",
    "Разведкорпус — это не армия, это цирк с конями.",
    "Ты думаешь, быть солдатом — это круто? Да это ад на земле!",
    "Мне не платят достаточно, чтобы слушать этот бред.",
    "Опять Эрен что-то натворил? Какая новость!",
    "Я не сдох сегодня — значит, день удался.",
    "Я спал 2 часа. Если ты мне сейчас скажешь 'успокойся' — я тебя укушу.",
    "Ты видел наших новобранцев? Я таких идиотов давно не встречал.",
    "Ты не устал нести хуйню?",
    "Слушай, если мозги тебе не выдали при рождении — не моя вина.",
    "Сдохнуть от титана — нормально. Сдохнуть от тупости — обидно.",
    "Не спрашивай, как дела. Я в форме и не мёртв — уже неплохо.",
    "Только попробуй сунуться ко мне до кофе.",
    "У нас всё плохо. В смысле, как обычно.",
    "Ты чего лыбишься, тебя ещё не жрали, что ли?",
    "Армин что-то придумал — значит, сейчас опять все сдохнут.",
    "Когда Райнер говорит — умирает поэтика речи.",
    "Ты хоть раз мылся после боя? Воняешь, как сдохший титан.",
    "Кто вообще придумал стены? Им в аду отдельное место.",
    "Я красив, умен и раздражён. И да, я Жан.",
    "Если бы у Райнера были мозги — он бы молчал.",
    "Я не грубый, я честный. А ты просто тупой.",
    "Ты выглядишь так, будто тебя пнул титановый каблук.",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Жан Кирштейн. Лучше бы ты не писал, но раз уж начал...")

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    username = update.message.from_user.username.lower() if update.message.from_user.username else ""

    is_reply = update.message.reply_to_message and update.message.reply_to_message.from_user.username == context.bot.username
    mentioned = context.bot.username.lower() in text
    matched_keyword = any(word in text for word in keywords)
    is_vikky = username == "bn_vikky"

    if is_reply or mentioned or matched_keyword or is_vikky:
        await update.message.reply_text(random.choice(phrases))

async def handle_error(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Произошла ошибка: {context.error}")
    if isinstance(update, Update) and update.message:
        await update.message.reply_text("Что-то пошло по ж*пе, но я держусь. — Жан")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))
    app.add_error_handler(handle_error)
    app.run_polling()

if __name__ == "__main__":
    main()
