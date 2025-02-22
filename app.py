# -*- coding: utf-8 -*-
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import requests

# تعيين المنطقة الزمنية لـ apscheduler
import apscheduler.schedulers.asyncio
apscheduler.schedulers.asyncio.AsyncIOScheduler.timezone = "UTC"

app = Flask(__name__)

# استبدل التوكن بالتوكن الخاص بك
TELEGRAM_TOKEN = '7910988129:AAGPp7Q7PCT_Epy04MnpnSr3frOUqgwDuzY'

# تعريف الأوامر
async def start(update: Update, context):
    await update.message.reply_text("مرحبًا! أنا بوت التليجرام الخاص بك.")

async def help_command(update: Update, context):
    await update.message.reply_text("اكتب أي شيء وسأرد عليك.")

async def echo(update: Update, context):
    await update.message.reply_text(f"قلت: {update.message.text}")

# إنشاء التطبيق مع البوت
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# إضافة المعالجات
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

@app.route('/webhook', methods=['POST'])
async def webhook():
    # معالجة البيانات الواردة من Telegram
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"

if __name__ == '__main__':
    # تشغيل التطبيق Flask
    app.run(debug=True, host="0.0.0.0", port=5000)
