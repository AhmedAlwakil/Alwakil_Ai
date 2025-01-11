from quart import Quart, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import pytz  # استيراد مكتبة pytz

app = Quart(__name__)

# استبدل هذا بـ API Token الخاص بك
TELEGRAM_TOKEN = '7910988129:AAEdaXIk-K2zeYbN_EjtiVCRaiwgVoQNuVA'

# تعريف الأمر /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('مرحبًا! أنا بوت الدردشة. كيف يمكنني مساعدتك؟')

# تعريف الأمر /help
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text('يمكنك التحدث معي مباشرة وسأحاول الرد عليك.')

# معالجة الرسائل النصية
async def echo(update: Update, context: CallbackContext):
    user_message = update.message.text
    # يمكنك هنا إضافة منطق معالجة الرسائل
    response = f"لقد قلت: {user_message}"
    await update.message.reply_text(response)

# إنشاء Application مع تكوين الخيوط (threads) والمنطقة الزمنية
application = (
    ApplicationBuilder()
    .token(TELEGRAM_TOKEN)
    .concurrent_updates(True)
    .job_queue(JobQueue())  # إضافة JobQueue مع المنطقة الزمنية
    .build()
)

# إضافة ال handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

@app.route('/webhook', methods=['POST'])
async def webhook():
    data = await request.get_json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return 'ok'

if __name__ == '__main__':
    app.run(port=8443)