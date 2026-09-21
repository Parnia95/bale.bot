import telebot
from telebot import apihelper
import os
from flask import Flask
import threading

apihelper.API_URL = "https://tapi.bale.ai/bot{0}/{1}"

TOKEN = "1781517105:rtMpb1kvTTfcIplCyAfSxoELHH55VlpeO3A"
ADMIN_ID = 1015391366

bot = telebot.TeleBot(TOKEN)

messages = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "سلام! پیام ناشناس بفرست، به دست صاحب ربات می‌رسه 😊")

@bot.message_handler(func=lambda m: True)
def anonymous(message):
    user_id = message.from_user.id
    text = message.text

    if user_id == ADMIN_ID:
        if message.reply_to_message:
            replied_id = message.reply_to_message.message_id
            target = messages.get(replied_id)
            if target:
                bot.send_message(target, f"💬 جواب:\n{text}")
                bot.reply_to(message, "✅ جواب فرستاده شد")
            else:
                bot.reply_to(message, "❌ پیدا نشد (آیدی پیام: {})".format(replied_id))
        else:
            bot.reply_to(message, "برای جواب، روی پیام ریپلای کن")
    else:
        sent = bot.send_message(ADMIN_ID, f"📩 پیام ناشناس:\n\n{text}")
        messages[sent.message_id] = user_id
        print("ذخیره شد: پیام {} ← کاربر {}".format(sent.message_id, user_id))
        bot.reply_to(message, "✅ پیامت رسید!")

app = Flask(__name__)

@app.route('/')
def home():
    return "ربات روشن است!"

def run_bot():
    print("ربات روشن شد...")
    bot.infinity_polling()

if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
