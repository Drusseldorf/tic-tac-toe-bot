from telebot.apihelper import ApiTelegramException
from bot_app import bot
from bot_app.bot_utils.message_builder import MessageBuilder
from bot_app.bot_utils.session_controller import SessionController


class RenderManager:
    def __init__(self, session_id: str):
        self._session_id = session_id

    def _bot_attrbt(self, last_message):
        return 'edit_message_text' if last_message else 'send_message'

    def render(self):
        session_controller = SessionController(self._session_id)
        game_session = session_controller.get_session()
        message_builder = MessageBuilder(last_message=game_session.last_message_id_user_one,
                                         game_board=game_session.game_board,
                                         session_id=self._session_id)
        chat_id = game_session.user_one_id

        try:
            sent = getattr(bot, self._bot_attrbt(game_session.last_message_id_user_one))(**message_builder.message_body(chat_id))
            session_controller.handle_state(sent)
        except ApiTelegramException as e:
            print(e)
