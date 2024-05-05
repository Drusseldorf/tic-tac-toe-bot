from bot_app import bot
from bot_app.bot_utils.session_controller import SessionController
from bot_app.bot_utils.render_field import RenderManager
from bot_app.bot_utils.move_handler import MoveHandler, MoveResult
from data_base.db_utils.session import Session
from bot_app.bot_utils.time_out_session_controller.check_timeout import expires_session_worker


@bot.message_handler(commands=['new_game', 'start'])
def start_new_game_session(message):
    game_session = Session.new(message.chat.id)
    RenderManager(game_session).render()


@bot.callback_query_handler(func=lambda call: True)
def move_callback_handler(call):
    pos_x, pos_y, session_id = call.data.split()

    session_controller = SessionController(session_id)
    game_session = session_controller.get_session()

    if game_session:
        move = MoveHandler(pos_x, pos_y, game_session)
        if move.make_move() is MoveResult.SUCCESS:
            RenderManager(game_session).render()


expires_session_worker()

bot.polling(none_stop=True)
