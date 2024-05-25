from telebot.apihelper import ApiTelegramException
from bot_app import bot
from bot_app.bot_utils.common_utils import number_of_chats
from bot_app.bot_utils.general_utils.message_builder import MessageBuilder
from bot_app.bot_utils.general_utils.game_session_controller import GameSessionController
from data_base.tables import GameSession
from logger.logger import log, Level


class RenderManager:
    def __init__(self, game_session: GameSession):
        self._game_session = game_session

    def render(self):
        """Renders a game field as a message with an inline keyboard"""
        message_builder = MessageBuilder(self._game_session)
        for i in range(number_of_chats(self._game_session)):
            try:
                sent = getattr(bot, self._bot_attrbt(i))(**message_builder.message_body()[i])
                self._set_new_last_message_id(sent.message_id, i)
            except ApiTelegramException as e:
                log.write(Level.ERROR, f'Message to Telegram API was unsuccessful: {e}')
        GameSessionController(self._game_session).update_game_session()

    def _bot_attrbt(self, count):
        last_messages = (self._game_session.last_message_id_user_one, self._game_session.last_message_id_user_two)
        return 'edit_message_text' if last_messages[count] else 'send_message'

    def _set_new_last_message_id(self, message_id, count):
        last_messages_attr = ('last_message_id_user_one', 'last_message_id_user_two')
        setattr(self._game_session, last_messages_attr[count], message_id)
