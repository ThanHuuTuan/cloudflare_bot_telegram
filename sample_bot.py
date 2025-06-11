from telegram_bot_api import TelegramBotAPI

def handle_update(update):
    if "data" in update:  # callback_query
        query_id = update["id"]
        chat_id = update["message"]["chat"]["id"]
        msg_id = update["message"]["message_id"]
        data = update["data"]

        # Trả lời nhanh callback
        bot.answer_callback_query(query_id, text=f"Bạn chọn: {data}")

        # Chỉnh sửa nội dung tin nhắn
        bot.edit_message_text(chat_id, msg_id, text=f"Bạn đã chọn: {data}")

    elif "text" in update:
        text = update["text"]
        chat_id = update["chat"]["id"]

        if text == "/voice":
            bot.send_voice(chat_id, "voice.ogg", caption="Đây là voice")
        elif text == "/video":
            bot.send_video(chat_id, "file_example_MP4_480_1_5MG.mp4", caption="Video demo")
        elif text == "/audio":
            bot.send_audio(chat_id, "audio.mp3", caption="Audio nhạc nền")
        elif text == "/inline":
            keyboard = {
                "inline_keyboard": [[
                    {"text": "Chọn A", "callback_data": "A"},
                    {"text": "Chọn B", "callback_data": "B"}
                ]]
            }
            bot.send_message(chat_id, "*Bấm chọn bên dưới:*", reply_markup=keyboard, parse_mode="Markdown")
        else:
            bot.reply(update, f"Bạn gửi: *{text}*", parse_mode="Markdown")

if __name__ == "__main__":
    TOKEN = "7175344-change-your-bot-telegram-token"
    bot = TelegramBotAPI(TOKEN)
    bot.polling(handle_update)
