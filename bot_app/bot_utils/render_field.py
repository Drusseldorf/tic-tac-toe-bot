from telebot.apihelper import ApiTelegramException
from bot_app import bot
from bot_app.bot_utils.message_builder import MessageBuilder
from bot_app.bot_utils.session_controller import SessionController
from data_base.tables import GameSession


class RenderManager:
    def __init__(self, game_session: GameSession):
        self._game_session = game_session

    def _bot_attrbt(self, last_message):
        return 'edit_message_text' if last_message else 'send_message'

    def render(self):
        message_builder = MessageBuilder(last_message=self._game_session.last_message_id_user_one,
                                         game_board=self._game_session.game_board,
                                         session_id=self._game_session.game_session,
                                         chat_id=self._game_session.user_one_chat_id)

        try:
            sent = getattr(bot, self._bot_attrbt(self._game_session.last_message_id_user_one))(**message_builder.message_body())
            SessionController(self._game_session).handle_state(sent)
        except ApiTelegramException as e:
            print(e)
