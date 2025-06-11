import requests
import time
import os
import traceback
import json

class TelegramBotAPI:
    def __init__(self, token):
        self.token = token
        self.api_url = f"https://YOUR-WORKER.workers.dev/bot{self.token}"
        self.offset = None

    def get_updates(self, timeout=30):
        try:
            params = {'timeout': timeout, 'offset': self.offset}
            r = requests.get(f"{self.api_url}/getUpdates", params=params, timeout=timeout + 5)
            r.raise_for_status()
            data = r.json()
            if data.get("ok"):
                updates = data["result"]
                if updates:
                    self.offset = updates[-1]["update_id"] + 1
                return updates
        except Exception as e:
            print(f"[get_updates] Error: {e}")
            traceback.print_exc()
        return []

    def send_message(self, chat_id, text, reply_to_message_id=None, reply_markup=None):
        try:
            payload = {
                "chat_id": chat_id,
                "text": text
            }
            if reply_to_message_id:
                payload["reply_to_message_id"] = reply_to_message_id
            if reply_markup:
                payload["reply_markup"] = json.dumps(reply_markup)

            r = requests.post(f"{self.api_url}/sendMessage", data=payload, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"[send_message] Error: {e}")
            traceback.print_exc()
        return {}

    def reply(self, message, text, reply_markup=None):
        try:
            chat_id = message["chat"]["id"]
            message_id = message["message_id"]
            return self.send_message(chat_id, text, reply_to_message_id=message_id, reply_markup=reply_markup)
        except Exception as e:
            print(f"[reply] Error: {e}")
            traceback.print_exc()
        return {}

    def send_photo(self, chat_id, photo, caption=None):
        return self._send_media(chat_id, photo, "sendPhoto", "photo", caption)

    def send_document(self, chat_id, document_path, caption=None):
        return self._send_media(chat_id, document_path, "sendDocument", "document", caption)

    def send_sticker(self, chat_id, sticker_path_or_url):
        return self._send_media(chat_id, sticker_path_or_url, "sendSticker", "sticker")

    def send_voice(self, chat_id, voice_path, caption=None):
        return self._send_media(chat_id, voice_path, "sendVoice", "voice", caption)

    def send_video(self, chat_id, video_path, caption=None):
        return self._send_media(chat_id, video_path, "sendVideo", "video", caption)

    def send_audio(self, chat_id, audio_path, caption=None):
        return self._send_media(chat_id, audio_path, "sendAudio", "audio", caption)

    def _send_media(self, chat_id, path_or_url, endpoint, field_name, caption=None):
        try:
            url = f"{self.api_url}/{endpoint}"
            if path_or_url.startswith("http"):
                payload = {"chat_id": chat_id, field_name: path_or_url}
                if caption:
                    payload["caption"] = caption
                r = requests.post(url, data=payload, timeout=15)
            elif os.path.exists(path_or_url):
                with open(path_or_url, 'rb') as f:
                    files = {field_name: f}
                    data = {"chat_id": chat_id}
                    if caption:
                        data["caption"] = caption
                    r = requests.post(url, files=files, data=data, timeout=30)
            else:
                print(f"[{endpoint}] File không tồn tại: {path_or_url}")
                return {}
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"[{endpoint}] Error: {e}")
            traceback.print_exc()
        return {}

    def answer_callback_query(self, callback_query_id, text=None, show_alert=False):
        try:
            payload = {
                "callback_query_id": callback_query_id,
                "show_alert": show_alert
            }
            if text:
                payload["text"] = text
            r = requests.post(f"{self.api_url}/answerCallbackQuery", data=payload, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"[answer_callback_query] Error: {e}")
            traceback.print_exc()
        return {}

    def edit_message_text(self, chat_id, message_id, text, reply_markup=None):
        try:
            payload = {
                "chat_id": chat_id,
                "message_id": message_id,
                "text": text
            }
            if reply_markup:
                payload["reply_markup"] = json.dumps(reply_markup)
            r = requests.post(f"{self.api_url}/editMessageText", data=payload, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"[edit_message_text] Error: {e}")
            traceback.print_exc()
        return {}

    def polling(self, handler_func, poll_interval=1):
        print("Bot is polling for updates...")
        try:
            while True:
                try:
                    updates = self.get_updates()
                    for update in updates:
                        try:
                            if "message" in update:
                                handler_func(update["message"])
                            elif "callback_query" in update:
                                handler_func(update["callback_query"])
                        except Exception as e:
                            print(f"[handler_func] Error: {e}")
                            traceback.print_exc()
                    time.sleep(poll_interval)
                except Exception as e:
                    print(f"[polling loop] Error: {e}")
                    traceback.print_exc()
                    time.sleep(5)
        except KeyboardInterrupt:
            print("Bot stopped by user.")
