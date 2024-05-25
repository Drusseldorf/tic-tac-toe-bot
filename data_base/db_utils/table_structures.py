from dataclasses import dataclass
from game_core.cells import Cell


@dataclass
class GameSessionData:
    user_one_id: str
    user_one_chat_id: str
    game_board: bytes
    session_uuid: str
    is_online: bool
    user_one_cell: Cell
    user_two_cell: Cell | None = None
    user_two_id: str | None = None
    user_two_chat_id: str | None = None
    last_message_id_user_one: str | None = None
    last_message_id_user_two: str | None = None
