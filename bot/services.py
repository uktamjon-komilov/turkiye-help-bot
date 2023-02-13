from django.conf import settings
import httpx as http_client

from .models import Profile


class TelegramService:
    def __init__(self, data):
        self.data = data
    
    @property
    def message(self):
        return self.data.get("message", {})
    
    @property
    def callback_query(self):
        return self.data.get("callback_query", {})
    
    @property
    def chat(self):
        return self.message.get("chat", {})
    
    @property
    def chat_id(self):
        chat_id = self.chat.get("id", 0)
        if chat_id == 0:
            chat_id = self.data \
                .get("callback_query", {}) \
                .get("message", {}) \
                .get("chat", {}) \
                .get("id", 0)
        return chat_id
    
    @property
    def username(self):
        return self.chat.get("username", "")
    
    @property
    def first_name(self):
        return self.chat.get("first_name", "")
    
    @property
    def last_name(self):
        return self.chat.get("last_name", "")
    

    @property
    def text(self):
        text = self.message.get("text", "")
        if text == "":
            text = self.callback_query.get("data", "")
        return text

    @property
    def message_id(self):
        message_id = self.message.get("message_id", "")
        if message_id == "":
            message = self.callback_query.get("message", {})
            message_id = message.get("message_id", "")
        return message_id

    @property
    def location(self):
        location = self.message.get("location", None)
        return location
    
    @property
    def contact(self):
        contact = self.message.get("contact", None)
        return contact

    @property
    def profile(self):
        profile = self.get_or_create_profile()
        return profile

    def get_or_create_profile(self) -> Profile:
        profiles = Profile.objects.filter(tg_id=self.chat_id)
        if profiles.exists():
            profile: Profile = profiles.first() # type: ignore
            return profile
        profile = Profile(
            tg_id=self.chat_id,
            tg_username=self.username,
            first_name=self.first_name,
            last_name=self.last_name
        )
        profile.save()
        return profile
    

    def check_step(self, step):
        profile: Profile = self.get_or_create_profile()
        return profile.step == step
    
    def set_step(self, step):
        profile: Profile = self.get_or_create_profile()
        profile.step = step
        profile.save()
    
    def get_step(self):
        profile: Profile = self.get_or_create_profile()
        return profile.step


class BotService:
    BASE_URL = "https://api.telegram.org/bot{}/".format(settings.BOT_TOKEN)
    
    def __init__(self, data):
        self.chat_id = TelegramService(data).chat_id
    

    def send_message(self, text, menu=None, inline=False):
        if self.chat_id < 0:
            return
        ACTION_VERB = "sendMessage"
        URL = "{}{}".format(self.BASE_URL, ACTION_VERB)
        DATA = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        if menu:
            if inline:
                DATA["reply_markup"] = {
                    "inline_keyboard": menu
                }
            else:
                DATA["reply_markup"] = {
                    "resize_keyboard": True,
                    "one_time_keyboard": True,
                    "keyboard": menu
                }
        response = http_client.post(
            URL,
            json=DATA
        )
        print(response.content)
        if response.status_code == 200:
            return True
        return False


    def delete_message(self, message_id):
        ACTION_VERB = "deleteMessage"
        URL = "{}{}".format(self.BASE_URL, ACTION_VERB)
        DATA = {
            "chat_id": self.chat_id,
            "message_id": message_id
        }
        response = http_client.post(
            URL,
            json=DATA
        )
        if response.status_code == 200:
            return True
        return False
    
    def send_location(self, longitude, latitude):
        ACTION_VERB = "sendLocation"
        URL = "{}{}".format(self.BASE_URL, ACTION_VERB)
        DATA = {
            "chat_id": self.chat_id,
            "latitude": latitude,
            "longitude": longitude
        }
        response = http_client.post(
            URL,
            json=DATA
        )
        if response.status_code == 200:
            return True
        return False
