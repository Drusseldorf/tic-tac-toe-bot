from data_base.session_operations import SessionOperations
from data_base.tables import LinkedUsers


class LinkedAccountsSessionController:
    def __init__(self, user_id: str):
        self._linked_users_session = SessionOperations.get_linked_users_session(user_id)
        if not self._linked_users_session:
            self._linked_users_session = SessionOperations.new_linked_users(user_id)

    def get_session(self) -> LinkedUsers:
        return self._linked_users_session

    def set_linked_user(self, user_id_to_link: str):
        self._linked_users_session.linked_users_id = f'{self._linked_users_session.linked_users_id} {user_id_to_link}'
        SessionOperations.update_linked_users(self._linked_users_session)
