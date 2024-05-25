from telebot import types
from telebot.apihelper import ApiTelegramException
from bot_app import bot
from bot_app.bot_utils.general_utils.callback_flags import CallBack
from bot_app.bot_utils.general_utils.callback_flags import Answer
from bot_app.bot_utils.common_utils import get_name
from config.text_templates.text_tamplate_obj import template
from logger.logger import log, Level


class InviteSender:
    def __init__(self, linked_user, initiator_user_name, initiator_user_chat_id):
        self._initiator_user_chat_id = initiator_user_chat_id
        self._initiator_user_name = initiator_user_name
        self._linked_user = linked_user

    def _prepare_options_as_markup_to_invite(self):
        buttons = [types.InlineKeyboardButton(text=template.INVITE_EVENT_TEXT.AGREE,
                                              callback_data=f'{Answer.AGREE.value} '
                                                            f'{self._initiator_user_chat_id} '
                                                            f'{self._linked_user} '
                                                            f'{CallBack.ANSWR_FLAG.value}'),
                   types.InlineKeyboardButton(text=template.INVITE_EVENT_TEXT.DISAGREE,
                                              callback_data=f'{Answer.DISAGREE.value} '
                                                            f'{self._initiator_user_chat_id} '
                                                            f'{self._linked_user} '
                                                            f'{CallBack.ANSWR_FLAG.value}')]
        markup = types.InlineKeyboardMarkup()
        markup.add(*buttons)
        return markup

    def _get_body_to_invite(self, markup):
        body = {
            'chat_id': self._linked_user,
            'text': template.INVITE_EVENT_TEXT.INVITE_MESSAGE.format(self._initiator_user_name),
            'reply_markup': markup
        }
        return body

    def _send_invite(self):
        markup = self._prepare_options_as_markup_to_invite()
        try:
            bot.send_message(**self._get_body_to_invite(markup))
        except ApiTelegramException as e:
            log.write(Level.ERROR, f'Message to Telegram API was unsuccessful: {e}')
            return False
        return True

    def _inform_initiator(self, result: bool):
        name = get_name(self._linked_user)
        text = template.INVITE_EVENT_TEXT.INVITE_WAS_SENT_SUCCESSFULLY.format(name) if result\
            else template.INVITE_EVENT_TEXT.INVITE_WAS_SENT_UNSUCCESSFULLY.format(name)
        try:
            bot.send_message(chat_id=self._initiator_user_chat_id, text=text)
        except ApiTelegramException as e:
            log.write(Level.ERROR, f'Message to Telegram API was unsuccessful: {e}')

    def event_handle(self):
        """

        """
        self._inform_initiator(self._send_invite())
