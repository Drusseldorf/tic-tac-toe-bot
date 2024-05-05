from bot_app import bot
from config.text_templates.russian import NoSessionText


class NoSessionHandler:
    def __init__(self, chat_id: str):
        self._chat_id = chat_id

    def handle_no_session(self):
        bot.send_message(self._chat_id, NoSessionText.INFORM_MESSAGE)
