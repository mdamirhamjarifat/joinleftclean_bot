import os
import telebot
from flask import Flask, request

# ----------------------------
# তোমার Bot Token (এখানেই বসানো আছে)
BOT_TOKEN = "7972514287:AAGLTVQgvgXfeywWmsXpsYegNVB_YmpFkjk"
# ----------------------------

bot = telebot.TeleBot(BOT_TOKEN, threaded=True)
app = Flask(__name__)

# ---------- Handlers ----------
@bot.message_handler(content_types=['new_chat_members'])
def delete_join_message(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        print(f"✅ Deleted join message in {getattr(message.chat, 'title', message.chat.id)}")
    except Exception as e:
        print(f"❌ Could not delete join message: {e}")

@bot.message_handler(content_types=['left_chat_member'])
def delete_left_message(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        print(f"✅ Deleted left message in {getattr(message.chat, 'title', message.chat.id)}")
    except Exception as e:
        print(f"❌ Could not delete left message: {e}")

# ---------- health endpoint ----------
@app.route("/", methods=["GET"])
def index():
    return "🤖 Bot is alive!"

# ---------- telegram webhook endpoint ----------
@app.route("/telegram_webhook", methods=["POST"])
def telegram_webhook():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

