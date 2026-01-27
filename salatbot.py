import os
from telegram.ext import Updater, CommandHandler

TOKEN = os.getenv("BOT_TOKEN")

def start(update, context):
    chat_id = update.message.chat_id

    with open('chat_ids.txt', 'a+') as file:
        file.seek(0)
        chat_ids = file.read().splitlines()
        if str(chat_id) not in chat_ids:
            file.write(f"{chat_id}\n")

    update.message.reply_text(
        "🤍 بوت منبه الصلاة على النبي ﷺ\n"
        "يتم إرسال تذكير تلقائي كل 30 دقيقة."
    )

def send_message_periodically(context):
    with open('chat_ids.txt', 'r') as file:
        chat_ids = file.read().splitlines()

    for chat_id in chat_ids:
        context.bot.send_message(
            chat_id=chat_id,
            text="اللهم صل وسلم وبارك على سيدنا محمد ﷺ"
        )

if __name__ == '__main__':
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    updater.job_queue.run_repeating(
        send_message_periodically,
        interval=1800,
        first=10
    )

    updater.start_polling()
    updater.idle()
