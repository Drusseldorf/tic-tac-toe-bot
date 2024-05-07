from telebot.apihelper import ApiTelegramException
from bot_app import bot
from bot_app.bot_utils.general_utils.message_builder import MessageBuilder
from bot_app.bot_utils.general_utils.game_session_controller import GameSessionController
from data_base.tables import GameSession


class RenderManager:
    def __init__(self, game_session: GameSession):
        self._game_session = game_session

    @staticmethod
    def _bot_attrbt(last_message):
        return 'edit_message_text' if last_message else 'send_message'

    def render(self):
        message_builder = MessageBuilder(self._game_session)
        number_of_chats = 2 if self._game_session.is_online else 1
        last_users_messages = (self._game_session.last_message_id_user_one, self._game_session.last_message_id_user_two)
        last_messages_attr = ('last_message_id_user_one', 'last_message_id_user_two')

        for i in range(number_of_chats):
            try:
                sent = getattr(bot, self._bot_attrbt(last_users_messages[i]))(**message_builder.message_body()[i])
                setattr(self._game_session, last_messages_attr[i], sent.message_id)
            except ApiTelegramException as e:
                print(e)

        GameSessionController(self._game_session).handle_state()
