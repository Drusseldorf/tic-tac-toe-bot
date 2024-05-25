from telebot.apihelper import ApiTelegramException
from bot_app.bot_utils.online_utils.linked_accs_session_controller import LinkedAccountsSessionController
from bot_app import bot
from bot_app.bot_utils.online_utils.invite_sender import InviteSender
from config.text_templates.text_tamplate_obj import template


class InviteNew:
    def __init__(self, initiator_user_id, linked_user, initiator_user_name, initiator_user_chat_id):
        self._initiator_user_id = initiator_user_id
        self._user_id_to_invite = linked_user
        self._initiator_user_chat_id = initiator_user_chat_id
        self._initiator_user_name = initiator_user_name
        self._session_controller = LinkedAccountsSessionController(self._initiator_user_id)

    def invite(self):
        """
        Handles the case when a user tries to invite another user to play by providing a user ID.
        """
        if self._trying_to_invite_himself():
            bot.send_message(self._initiator_user_chat_id, template.INVITING_BY_ID.INVITING_HIMSELF)
        elif self._is_user_known_to_bot():
            InviteSender(self._user_id_to_invite, self._initiator_user_name, self._initiator_user_chat_id).event_handle()
            self._add_user_as_linked()
        else:
            self._inviting_unkown_user()

    @staticmethod
    def provide_user_id_to_invite(initiator_user_chat_id):
        bot.send_message(initiator_user_chat_id, template.INVITING_BY_ID.GIVE_ME_USER_ID)

    def _is_user_known_to_bot(self):
        try:
            bot.get_chat(self._user_id_to_invite)
        except ApiTelegramException:
            return False
        return True

    def _is_user_already_in_list(self):
        users_str = self._session_controller.get_session().linked_users_id
        if users_str:
            return self._user_id_to_invite in users_str.split()
        else:
            return False

    def _add_user_as_linked(self):
        """
        Adds user to a linked users list
        """
        if not self._is_user_already_in_list():
            self._session_controller.set_linked_user(self._user_id_to_invite)

    def _inviting_unkown_user(self):
        bot.send_message(self._initiator_user_chat_id, template.INVITING_BY_ID.UNKOWN_USER)

    def _trying_to_invite_himself(self):
        return str(self._user_id_to_invite) == str(self._initiator_user_id)
