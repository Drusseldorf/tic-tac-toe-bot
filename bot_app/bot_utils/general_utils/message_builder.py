from telebot import types
from bot_app.bot_utils.general_utils.cell_image_mapping import Mapping
from config.text_templates.russian import MoveTurnText, MoveTurnTextOnline
from data_base.tables import GameSession
from game_utils.field import GameBoard
from game_utils.game_state_handler import State, GameState
from game_utils.make_move import Move
from bot_app.bot_utils.general_utils.callback_flags import CallBack
from bot_app.bot_utils.online_utils.common_utils import get_name


class MessageBuilder:
    def __init__(self, game_session: GameSession):
        self._game_session = game_session
        self._move_obj = Move(self._game_session.game_board)

    def _game_board_into_buttons(self):
        buttons = []
        pos_x = 0
        pos_y = 0
        for row in GameBoard.turn_into_list(self._game_session.game_board):
            pos_x += 1
            for cell in row:
                pos_y += 1
                cell_emoji = Mapping.cell_into_emoji(cell)
                button = types.InlineKeyboardButton(text=cell_emoji,
                                                    callback_data=f'{pos_x - 1} '
                                                                  f'{pos_y - 1} '
                                                                  f'{self._game_session.game_session} '
                                                                  f'{CallBack.MOVE_FLAG}')
                buttons.append(button)
            pos_y = 0
        return buttons

    def _prepare_buttons(self):
        buttons = self._game_board_into_buttons()
        markup = types.InlineKeyboardMarkup(row_width=len(GameBoard.turn_into_list(self._game_session.game_board)))
        markup.add(*buttons)
        return markup

    def _text_attrbt(self):
        game_state = GameState(self._game_session.game_board).state
        if game_state is State.IN_PROGRESS:
            return 'NEXT_TURN'
        elif game_state is State.DRAW:
            return 'DRAW'
        else:
            return 'WON'

    def _get_current_move_user_name(self):
        if self._move_obj.whos_turn().name == self._game_session.user_one_cell:
            user_id = self._game_session.user_one_id
        else:
            user_id = self._game_session.user_two_id
        if GameState(self._game_session.game_board).state is not State.IN_PROGRESS:
            if self._move_obj.last_turn().name == self._game_session.user_one_cell:
                user_id = self._game_session.user_one_id
            else:
                user_id = self._game_session.user_two_id

        return get_name(user_id)

    def _get_text(self):
        if self._game_session.is_online:
            return getattr(MoveTurnTextOnline, self._text_attrbt()).format(self._get_current_move_user_name())
        else:
            return getattr(MoveTurnText, self._text_attrbt())

    def _text_cell_or_draw(self):
        game_state = GameState(self._game_session.game_board).state
        if game_state is State.IN_PROGRESS:
            return Mapping.cell_into_emoji(self._move_obj.whos_turn())
        elif game_state is State.DRAW:
            return ''
        else:
            return Mapping.cell_into_emoji(self._move_obj.last_turn())

    def message_body(self) -> list[dict]:
        tuple_of_message_bodies = []
        last_messages = [self._game_session.last_message_id_user_one, self._game_session.last_message_id_user_two]
        chat_ids = [self._game_session.user_one_chat_id, self._game_session.user_two_chat_id]
        last_message_ids = [self._game_session.last_message_id_user_one, self._game_session.last_message_id_user_two]
        number_of_chats = 2 if self._game_session.is_online else 1

        for i in range(number_of_chats):

            body = {
                'chat_id': chat_ids[i],
                'reply_markup': self._prepare_buttons(),
                'text': f'{self._get_text()} {self._text_cell_or_draw()}'
            }
            if last_messages[i]:
                body['message_id'] = last_message_ids[i]
            tuple_of_message_bodies.append(body)

        return tuple_of_message_bodies
