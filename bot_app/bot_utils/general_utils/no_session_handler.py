from telebot.apihelper import ApiTelegramException

from bot_app import bot
from config.text_templates.russian import NoSessionText


class NoSessionHandler:
    def __init__(self, chat_id: str, message_id: str):
        self._message_id = message_id
        self._chat_id = chat_id

    def inform_no_session(self):
        try:
            bot.edit_message_text(chat_id=self._chat_id, text=NoSessionText.INFORM_MESSAGE, message_id=self._message_id)
        except ApiTelegramException as e:
            print(e)
