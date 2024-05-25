from typing import List
from telebot.apihelper import ApiTelegramException
from bot_app import bot
from bot_app.bot_utils.general_utils.callback_flags import Answer
from bot_app.bot_utils.common_utils import get_name
from config.text_templates.text_tamplate_obj import template
from logger.logger import Level, log


class AnswerHandler:
    def __init__(self, answer: str, initiator_user_chat_id: str, linked_user_id: str):
        self._linked_user_id = linked_user_id
        self._initiator_user_chat_id = initiator_user_chat_id
        self._answer = getattr(Answer, answer).name
        self._linked_user_name = get_name(self._linked_user_id)

    def handle_answer_is_agree(self) -> bool:
        """
        Handles user's response to an invite and informs users of the decision.
        :return: True if user agreed to play, or False if user declined the invite.
        """
        self._inform_users()
        return self._answer is Answer.AGREE.value

    def _get_body(self) -> List[dict]:
        body = []

        text_for_invited_user = template.INVITE_ANSWER_TEXT.INVITED_USER_AGREE if self._answer is Answer.AGREE.value \
            else template.INVITE_ANSWER_TEXT.INVITED_USER_DISAGREE

        body_to_invited_user = {
            'chat_id': self._linked_user_id,
            'text': text_for_invited_user
        }

        text_for_initiator_user = template.INVITE_ANSWER_TEXT.INITIATOR_USER_AGREE.format(self._linked_user_name) if self._answer is Answer.AGREE.value \
            else template.INVITE_ANSWER_TEXT.INITIATOR_USER_DISAGREE.format(self._linked_user_name)

        body_to_initiator_user = {
            'chat_id': self._initiator_user_chat_id,
            'text': text_for_initiator_user
        }

        body.append(body_to_invited_user)
        body.append(body_to_initiator_user)

        return body

    def _inform_users(self):
        for i in range(2):
            try:
                bot.send_message(**self._get_body()[i])
            except ApiTelegramException as e:
                log.write(Level.ERROR, f'Message to Telegram API was unsuccessful: {e}')
