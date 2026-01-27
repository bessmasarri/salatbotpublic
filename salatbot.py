import os
from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackContext, Filters 
from telegram.error import TelegramError

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN غير موجود في Environment Variables")

WELCOME_TEXT = (
    "🤍 فضل الصلاة على النبي ﷺ:\n\n"
    "فما تزال تُصلّي على النبي ﷺ\n"
    "تُصلّي.. تُصلّي..\n"
    "حتى لا يبقى في قلبك همٌّ\n"
    "إلّا وأخرجه الله منك كأنّه لم يكن.\n\n"
    "لينطبق عليك حديث فضل الصلاة على النبي ﷺ ♥️\n\n"
    "«إذن تُكفى همَّك ويُغفر لك ذنبك»\n\n"
    "هذا رسولٌ قد تجلّى نوره\n"
    "حتى تلاشتْ ظلمةُ الأعماقِ\n\n"
    "صلّى عليكَ الله دومًا كلّما\n"
    "رَمَشَتْ على الأزمانِ كلّ حداق\n\n"
    "\n"
    "🕰 اختر وقت التذكير (بالساعات):\n\n"
    "🔹 0.1 = 6 دقائق\n"
    "🔹 0.25 = 15 دقيقة\n"
    "🔹 0.5 = 30 دقيقة (نصف ساعة)\n"
    "🔹 1 = ساعة واحدة\n"
    "🔹 2 = ساعتان\n"
    "🔹 حتى 23 ساعة\n\n"
    "✍️ اكتب الرقم فقط (مثال: 0.5 أو 1 أو 2)\n"
    "🔁 لتغيير الوقت لاحقًا اكتب: وقت"
)


SALAT_TEXT = "اللهم صل وسلم وبارك على سيدنا محمد ﷺ"

# ───────── إرسال الصلاة ─────────
def send_salat(context: CallbackContext, chat_id=None):
    # si on a context.job, on prend le chat_id de là
    if chat_id is None:
        chat_id = context.job.context
    try:
        context.bot.send_message(chat_id=chat_id, text=SALAT_TEXT)
    except TelegramError:
        jobs = context.job_queue.get_jobs_by_name(str(chat_id))
        for job in jobs:
            job.schedule_removal()
        print(f"تم حذف المستخدم {chat_id} (حظر البوت)")


# ───────── start (يصل تلقائيًا عند الدخول) ─────────
def start(update: Update, context: CallbackContext):
    update.message.reply_text(WELCOME_TEXT)

# ───────── تغيير الوقت ─────────
def ask_time(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🕰 ارسل الوقت الجديد بالساعات (من 0.1 إلى 23)\n"
        "مثال: 0.5 = نصف ساعة"
    )

# ───────── استقبال الرقم ─────────
def handle_time(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text.strip()

    try:
        hours = float(text)
        if not (0.1 <= hours <= 23):
            raise ValueError
    except ValueError:
        update.message.reply_text(
            "❌ إدخال غير صالح\n"
            "اكتب رقمًا بين 0.1 و 23 ساعة فقط"
        )
        return

    seconds = hours * 3600

    # حذف أي تذكير قديم
    jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in jobs:
        job.schedule_removal()

    # إضافة تذكير جديد
    context.job_queue.run_repeating(
        send_salat,
        interval=seconds,
        first=1,
        context=chat_id,
        name=str(chat_id)
    )

    update.message.reply_text(
        f"✅ سيتم إرسال الصلاة على النبي ﷺ كل {hours} ساعة\n"
        "يمكنك تغيير الوقت في أي وقت بكتابة: وقت"
    )

    send_salat(context,chat_id)

# ───────── main ─────────
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.regex("^وقت$"), ask_time))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_time))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
