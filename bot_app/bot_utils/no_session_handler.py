from bot_app import bot
from config.text_templates.russian import NoSessionText


class NoSessionHandler:
    def __init__(self, chat_id: str, message_id: str):
        self._message_id = message_id
        self._chat_id = chat_id

    def inform_no_session(self):
        bot.send_message(self._chat_id, NoSessionText.INFORM_MESSAGE, reply_to_message_id=self._message_id)
