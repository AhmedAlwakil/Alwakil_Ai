# -*- coding: utf-8 -*-
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from pytz import utc
from git import Repo
import os

# تعيين المنطقة الزمنية لـ apscheduler
import apscheduler.schedulers.asyncio
apscheduler.schedulers.asyncio.AsyncIOScheduler.timezone = utc

app = Flask(__name__)

# استبدل التوكن بالتوكن الخاص بك
TELEGRAM_TOKEN = '7910988129:AAGPp7Q7PCT_Epy04MnpnSr3frOUqgwDuzY'

# رابط المستودع
repo_url = "https://github.com/AhmedAlwakil/Alwakil_Ai.git"
repo_path = "./local_repo"

# استنساخ المستودع من GitHub إذا لم يكن موجودًا
if not os.path.exists(repo_path):
    try:
        repo = Repo.clone_from(repo_url, repo_path)
        print("تم استنساخ المستودع بنجاح!")
    except Exception as e:
        print(f"فشل في استنساخ المستودع: {str(e)}")
else:
    print("المستودع موجود بالفعل.")

# تعريف الأوامر للبوت
async def start(update: Update, context):
    await update.message.reply_text("مرحبًا! أنا بوت التليجرام الخاص بك.")

async def help_command(update: Update, context):
    await update.message.reply_text("اكتب أي شيء وسأرد عليك.")

async def echo(update: Update, context):
    await update.message.reply_text(f"قلت: {update.message.text}")

# تهيئة التطبيق وإضافة الأوامر
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

@app.route('/webhook', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)
