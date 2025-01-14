import requests

webhook_url = "https://cuddly-sunset-house.glitch.me/webhook"  # ضع الرابط الخاص بك هنا
TELEGRAM_TOKEN = "7910988129:AAGPp7Q7PCT_Epy04MnpnSr3frOUqgwDuzY"

# إعداد webhook باستخدام POST
url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
data = {"url": webhook_url}

response = requests.post(url, data=data)

print(response.json())  # لمعرفة النتيجة
