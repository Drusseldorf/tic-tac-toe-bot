from telebot import types
from telebot.apihelper import ApiTelegramException
from bot_app.bot_utils.general_utils.callback_flags import CallBack
from bot_app import bot
from config.text_templates.text_tamplate_obj import template
from data_base.tables import LinkedUsers
from bot_app.bot_utils.common_utils import get_name
from logger.logger import log, Level


class InitiateInvite:
    def __init__(self, linked_users_session: LinkedUsers):
        self._linked_users_session = linked_users_session

    def event_handle(self, message):
        """
        Handles invite event. Sends list of linked users as an inline keyboard.
        Sends inform message If user dont have any linked users.
        :param message: telegram callback message
        """
        markup = self._prepare_list_of_users_to_invite_as_markup(message)
        try:
            bot.send_message(**self._get_body(message, markup))
        except ApiTelegramException as e:
            log.write(Level.ERROR, f'Message to Telegram API was unsuccessful: {e}')

    def _prepare_list_of_users_to_invite_as_markup(self, message):

        if not self._linked_users_session:
            return

        if not self._linked_users_session.linked_users_id:
            return

        list_of_linked_users = set(self._linked_users_session.linked_users_id.split())

        initiator_user_name = message.from_user.first_name
        initiator_user_chat_id = message.chat.id
        buttons = []

        for linked_user in list_of_linked_users:
            user_name_to_invite = get_name(linked_user)
            button = types.InlineKeyboardButton(text=user_name_to_invite,
                                                callback_data=f'{linked_user} '
                                                              f'{initiator_user_name} '
                                                              f'{initiator_user_chat_id} '
                                                              f'{CallBack.INVT_FLAG.value}')
            buttons.append(button)

        markup = types.InlineKeyboardMarkup()
        markup.add(*buttons)

        return markup

    @staticmethod
    def _get_body(message, markup) -> dict:
        body = {
            'chat_id': message.chat.id,
            'text': template.INVITE_EVENT_TEXT.NO_LINKED_USERS_YET
        }
        if markup:
            body['reply_markup'] = markup
            body['text'] = template.INVITE_EVENT_TEXT.CHOOSE_USER_MESSAGE
        return body
