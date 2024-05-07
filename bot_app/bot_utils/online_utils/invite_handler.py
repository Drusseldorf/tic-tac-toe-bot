from telebot import types
from telebot.apihelper import ApiTelegramException
from config.text_templates.russian import InviteEventText
from bot_app.bot_utils.general_utils.callback_flags import CallBack
from bot_app import bot
from data_base.tables import LinkedUsers
from bot_app.bot_utils.online_utils.common_utils import get_name


class InitiateInvite:
    def __init__(self, linked_users_session: LinkedUsers):
        self._list_of_linked_users = linked_users_session.linked_users_id

    def _prepare_list_of_users_to_invite_as_markup(self, message):
        list_of_linked_users = self._list_of_linked_users.split()
        initiator_user_name = f'{message.from_user.first_name}'
        initiator_user_chat_id = message.chat.id
        buttons = []

        for linked_user in list_of_linked_users:
            user_name_to_invite = get_name(linked_user)
            button = types.InlineKeyboardButton(text=user_name_to_invite,
                                                callback_data=f'{linked_user} '
                                                              f'{initiator_user_name} '
                                                              f'{initiator_user_chat_id} '
                                                              f'{CallBack.INVT_FLAG.name}')
            buttons.append(button)

        markup = types.InlineKeyboardMarkup()
        markup.add(*buttons)

        return markup

    def _get_body(self, message, markup) -> dict:
        body = {
            'chat_id': message.chat.id,
            'text': InviteEventText.CHOOSE_USER_MESSAGE,
            'reply_markup': markup
        }
        if not self._list_of_linked_users:
            del body['reply_markup']
            body['text'] = InviteEventText.NO_LINKED_USERS_YET
        return body

    def event_handle(self, message):

        markup = self._prepare_list_of_users_to_invite_as_markup(message)

        try:
            bot.send_message(**self._get_body(message, markup))
        except ApiTelegramException as e:
            print(f'InitiateInvite.event_handle failed:\n{e}')
