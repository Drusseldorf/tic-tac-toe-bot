from bot_app import bot
from bot_app.bot_utils.session_controller import SessionController
from bot_app.bot_utils.render_field import RenderManager
from bot_app.bot_utils.move_handler import MoveHandler, MoveResult
from data_base.db_utils.session import Session
from bot_app.bot_utils.time_out_session_controller.check_timeout import expires_session_worker
from bot_app.bot_utils.no_session_handler import NoSessionHandler


@bot.message_handler(commands=['new_game', 'start'])
def start_new_game_session(message):
    game_session = Session.new(user1_id=message.from_user.id,
                               user1_chat_id=message.chat.id,
                               is_online=False)
    RenderManager(game_session).render()


@bot.message_handler(commands=['new_online_game'])
def start_new_online_game_session(message):
    pass


@bot.callback_query_handler(func=lambda call: True)
def move_callback_handler(call):
    pos_x, pos_y, session_id = call.data.split()

    session_controller = SessionController(session_id)
    game_session = session_controller.get_session()

    if game_session:
        move = MoveHandler(pos_x, pos_y, game_session)
        if move.make_move() is MoveResult.SUCCESS:
            RenderManager(game_session).render()
    else:
        NoSessionHandler(call.message.chat.id, call.message.message_id).inform_no_session()


expires_session_worker()

bot.polling(none_stop=True)
