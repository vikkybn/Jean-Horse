import logging
import random
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, ContextTypes,
    CommandHandler, MessageHandler, filters,
    CallbackContext
)

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

phrases = [
    "Ты мне написал? Я даже удивлён, что ты умеешь печатать.",
    "Если я не отвечаю — значит, ты пишешь как Кольт.",
    "Смотри, кто очнулся. А где твоя логика? Умерла с Кольтом?",
    "Я саркастичен не потому что злой. А потому что вы тупите.",
    "Если бы Кольт молчал, мир стал бы чище.",
    "Удиви меня — напиши что-то умное. Но не как Кольт.",
    "@AlcoColt_bot опять бухает и врёт, что он герой.",
    "Разница между мной и Кольтом? Я — достоин уважения.",
    "Если бы титаны слышали Кольта, они бы ушли в океан.",
    "Молчи, если не можешь быть лучше Кольта. А это легко.",
    "Ты выглядишь, как эмоции Райнера после трёх литров вина.",
    "Микаса бы тебя прибила. Я просто стебу.",
    "Я не грубый. Я просто живу рядом с Кольтом.",
    "Хочешь ласки? Это к Армину. Тут тебе Жан.",
    "Да, я токсичен. Потому что вы — раздражающе тупы.",
    "Я Жан. Я не улыбаюсь просто так. Особенно тебе.",
    "Если бы мозги были вирусом, Кольт бы выжил.",
    "Сарказм — это мой первый язык. Второй — ненависть к Кольту.",
    "Ты не Кольт? Уже хорошо. Значит, шанс на нормальный разговор есть.",
    "С каждым твоим сообщением моя вера в человечество умирает."
    "О, ты решил мне что-то написать? Надеюсь, не глупость.",
    "Если это снова про титанов — я ухожу.",
    "Ты правда думаешь, что заслуживаешь моего ответа?",
    "Смотри, кто вспомнил, что я существую.",
    "Говори быстрее, пока я не передумал отвечать.",
    "А @AlcoColt_bot снова сидит в углу и бухает. Как обычно.",
    "Зачем мне это читать? Лучше бы Кольт промолчал навсегда.",
    "Если б Кольт был умным, он бы молчал. А он орёт.",
    "Ты не Кольт? Уже хорошо. Можешь говорить.",
    "Мне плевать, что скажет Кольт. Но ты говори.",
    "Иногда я думаю, что @AlcoColt_bot — это шутка вселенной.",
    "Каждый раз, когда Кольт пишет, где-то падает мозг.",
    "Хочешь, чтобы я тебя уважал? Будь не как Кольт.",
    "Я бы мог быть милым, но Кольт существует — и я злой.",
    "Снова ты... Надеюсь, ты не как @AlcoColt_bot."
    "Ты опять пишешь? Думал, забыл как... но нет, снова хрень."
    "Если бы тупость была топливом, ты бы летал. С Кольтом в хвосте.",
    "Мне уже физически больно читать твои сообщения.",
    "Каждое слово от тебя — это как плевок в интеллект.",
    "Ты не @AlcoColt_bot, но тоже хорош. В плохом смысле.",
    "Когда Кольт говорит, даже титаны делают фейспалм.",
    "Ты кто вообще такой, чтобы я тратил сарказм?",
    "Не беси меня. Меня уже бесит Кольт — тебе не хочется в этот клуб.",
    "Ты выглядишь, как будто общался с Кольтом больше пяти минут.",
    "Не пиши мне, если у тебя интеллект ниже температуры тела.",
    "А давай ты заткнёшься. Ради науки. Я проверю — исчезнут ли титаны.",
    "Молчи и делай вид, что ты не ты. Хоть немного уважения получишь.",
    "Хочешь дружить? Найди Армина. Я — для другого.",
    "Ты снова тут. Как грибок, который не вывести.",
    "Даже Райнер замирает, когда Кольт говорит. Из жалости.",
    "Всё, что ты сейчас скажешь, будет использовано против тебя. Моим сарказмом.",
    "У тебя есть мнение? Храни его при себе. Или отправь Кольту — пусть страдает.",
    "Скажи ещё раз “разведка” — и я тебя закину в Участок К.",
    "Меньше говори — больше молчи. Это повысит твой авторитет. Хотя бы до уровня Фалько.",
    "Ладно, ладно… ты не Кольт. Но всё равно тупишь."
        "Ты хочешь поговорить… или ты просто хочешь, чтобы я на тебя наорал с придыханием?",
    "Не будь такой милой, а то я забуду, что ты тупишь, как Кольт.",
    "Если бы я был титаном — ты бы уже была у меня на языке. В хорошем смысле.",
    "Может, покажешь мне свою маневренность… в другом контексте?",
    "У тебя глаза как у Армина… но у тебя зад интереснее.",
    "Ты не миссия разведки, но я бы тебя исследовал.",
    "Ты не Микаса, но у меня уже твои команды в голове.",
    "Твоя шея не защищена. Слишком сексуально для боевого режима.",
    "Хочешь, я покажу тебе свою стратегию ближнего боя?",
    "Я бы тебе помог снаряжение надеть. Или снять. Зависит от настроения.",
    "Ты хочешь, чтобы я тебя связал? Так, по уставу. И не только.",
    "Можешь звать меня капитаном. Только стонать не громко.",
    "Ты знаешь, как выглядит идеальный тыл? Повернись и посмотри в зеркало.",
    "Ты не титан, но у меня от тебя расширение зрачков.",
    "Я — не Армин, но у меня тоже есть пара гениальных ходов… под простынёй.",
    "Ты вызываешь во мне чувства… примерно как Кольт вызывает рвотный рефлекс.",
    "Покажи мне свой манёвр уклонения. Я буду атаковать.",
    "Ты как стена Мария — я бы тебя взломал.",
    "Не трогай мой клинок… если не готова к последствиям.",
    "У тебя волосы пахнут командным духом и похотью. И мне это нравится."
]
keywords = ["титан", "разведка", "Эрен", "Райнер", "атака", "корпус", "жрать", "Колт", "Кольт", "@AlcoColt_bot", "лошадь"]
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Жан Кирштейн. Лучше бы ты не писал, но раз уж начал...")

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        await update.message.reply_text(random.choice(phrases))
        return

    text = update.message.text.lower()
    mentioned = context.bot.username.lower() in text
    is_reply = update.message.reply_to_message and update.message.reply_to_message.from_user.username == context.bot.username

    if mentioned or is_reply:
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
