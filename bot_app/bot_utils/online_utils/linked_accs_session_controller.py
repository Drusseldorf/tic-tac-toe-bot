from data_base.db_utils.session import Session
from data_base.tables import LinkedUsers


class LinkedAccountsSessionController:
    def __init__(self, user_id: str):
        self._linked_users_session = Session.get_linked_users_session(user_id)

    def get_session(self) -> LinkedUsers:
        return self._linked_users_session

    def set_linked_user(self, user_id_to_link: str):
        Session.set_new_linked_user(self._linked_users_session, user_id_to_link)
