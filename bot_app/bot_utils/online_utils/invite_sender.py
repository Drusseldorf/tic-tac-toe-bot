from telebot import types
from telebot.apihelper import ApiTelegramException
from bot_app import bot
from bot_app.bot_utils.general_utils.callback_flags import CallBack
from config.text_templates.russian import InviteEventText
from bot_app.bot_utils.general_utils.callback_flags import Answer
from bot_app.bot_utils.online_utils.common_utils import get_name


class InviteSender:
    def __init__(self, linked_user, initiator_user_name, initiator_user_chat_id):
        self._initiator_user_chat_id = initiator_user_chat_id
        self._initiator_user_name = initiator_user_name
        self._linked_user = linked_user

    def _prepare_options_as_markup_to_invite(self):
        buttons = [types.InlineKeyboardButton(text=InviteEventText.AGREE,
                                              callback_data=f'{Answer.AGREE.name} '
                                                            f'{self._initiator_user_chat_id} '
                                                            f'{self._linked_user} '
                                                            f'{CallBack.ANSWR_FLAG.name}'),
                   types.InlineKeyboardButton(text=InviteEventText.DISAGREE,
                                              callback_data=f'{Answer.DISAGREE.name} '
                                                            f'{self._initiator_user_chat_id} '
                                                            f'{self._linked_user} '
                                                            f'{CallBack.ANSWR_FLAG.name}')]
        markup = types.InlineKeyboardMarkup()
        markup.add(*buttons)
        return markup

    def _get_body_to_invite(self, markup):
        body = {
            'chat_id': self._linked_user,
            'text': InviteEventText.INVITE_MESSAGE.format(self._initiator_user_name),
            'reply_markup': markup
        }
        return body

    def _send_invite(self):
        markup = self._prepare_options_as_markup_to_invite()
        try:
            bot.send_message(**self._get_body_to_invite(markup))
        except ApiTelegramException as e:
            print(f'InviteSender._send_invite failed here:\n{e}')
            return False
        return True

    def _inform_initiator(self, result: bool):
        name = get_name(self._linked_user)
        text = InviteEventText.INVITE_WAS_SENT_SUCCESSFULLY.format(name) if result\
            else InviteEventText.INVITE_WAS_SENT_UNSUCCESSFULLY.format(name)
        try:
            bot.send_message(chat_id=self._initiator_user_chat_id, text=text)
        except ApiTelegramException as e:
            print(f'InviteSender._inform_initiator failed:\n{e}')

    def event_handle(self):
        self._inform_initiator(self._send_invite())
