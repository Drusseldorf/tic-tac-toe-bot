from bot_app import bot
from bot_app.bot_utils.cell_image_mapping import Mapping
from game_entities.field import GameBoard
from game_entities.utils.move_handler import Move
from config.text_templates.russian import Text
from data_base.db_utils.session import Session
from game_entities.utils.game_state_handler import State, GameState
from telebot import types


class Field:

    def __init__(self,
                 session_id: str,
                 chat_id: str,
                 game_board: str):
        self.__session_id = session_id
        self.__mapping_obj = Mapping()
        self.__chat_id = chat_id
        self.__game_board = GameBoard.turn_into_list(game_board)
        self.__whos_turn = Move(game_board).whos_turn()
        self.__last_move = Move(game_board).last_turn()

    def __game_board_into_buttons(self):

        buttons = []
        pos_x = 0
        pos_y = 0

        for row in self.__game_board:
            pos_x += 1
            for cell in row:
                pos_y += 1
                cell_emoji = self.__mapping_obj.cell_into_emoji(cell)
                button = types.InlineKeyboardButton(text=cell_emoji,
                                                    callback_data=f'{pos_x - 1} {pos_y - 1} {self.__session_id}')
                buttons.append(button)
            pos_y = 0
        return buttons

    def _check_last_message(self):
        return Session.get_last_message(self.__session_id)

    def _game_state(self):
        return GameState(GameBoard.turn_into_str(self.__game_board)).state

    def render(self):
        buttons = self.__game_board_into_buttons()
        markup = types.InlineKeyboardMarkup(row_width=len(self.__game_board))
        markup.add(*buttons)
        who_next = self.__mapping_obj.cell_into_emoji(self.__whos_turn)
        who_was_last = self.__mapping_obj.cell_into_emoji(self.__last_move)
        if self._check_last_message():
            if self._game_state() == State.IN_PROGRESS:
                sent = bot.edit_message_text(chat_id=self.__chat_id,
                                             message_id=self._check_last_message(),
                                             reply_markup=markup,
                                             text=f'{Text.NEXT_TURN} {who_next}')
            elif self._game_state() == State.DRAW:
                sent = bot.edit_message_text(chat_id=self.__chat_id,
                                             message_id=self._check_last_message(),
                                             reply_markup=markup,
                                             text=f'{Text.DRAW}')
            else:
                sent = bot.edit_message_text(chat_id=self.__chat_id,
                                             message_id=self._check_last_message(),
                                             reply_markup=markup,
                                             text=f'{Text.WON} {who_was_last}')
        else:
            sent = bot.send_message(chat_id=self.__chat_id,
                                    reply_markup=markup,
                                    text=f'{Text.NEXT_TURN} {who_next}')

        Session.set_last_message(self.__session_id, sent.message_id)

    def render_online(self):
        pass
