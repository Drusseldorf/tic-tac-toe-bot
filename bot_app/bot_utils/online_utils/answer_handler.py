from telebot.apihelper import ApiTelegramException
from bot_app import bot
from bot_app.bot_utils.general_utils.callback_flags import Answer
from config.text_templates.russian import InviteAnswerText
from bot_app.bot_utils.online_utils.common_utils import get_name


class AnswerHandler:
    def __init__(self, answer: str, initiator_user_chat_id: str, linked_user_id: str):
        self._linked_user_id = linked_user_id
        self._initiator_user_chat_id = initiator_user_chat_id
        self._answer = getattr(Answer, answer).name
        self._linked_user_name = get_name(self._linked_user_id)

    def _get_body(self):
        body = []
        body_to_invited_user = {
            'chat_id': self._linked_user_id,
            'text': InviteAnswerText.INVITED_USER_AGREE if self._answer is Answer.AGREE.name else InviteAnswerText.INVITED_USER_DISAGREE
        }

        body_to_initiator_user = {
            'chat_id': self._initiator_user_chat_id,
            'text': InviteAnswerText.INITIATOR_USER_AGREE.format(self._linked_user_name) if self._answer is Answer.AGREE.name else InviteAnswerText.INITIATOR_USER_DISAGREE.format(self._linked_user_name)
        }

        body.append(body_to_invited_user)
        body.append(body_to_initiator_user)

        return body

    def _inform_users(self):
        for i in range(2):
            try:
                bot.send_message(**self._get_body()[i])
            except ApiTelegramException as e:
                print(f'AnswerHandler._inform_users_if_disagree: {e}')

    def handle_answer_is_agree(self):
        self._inform_users()
        print(self._answer)
        return self._answer is Answer.AGREE.name
