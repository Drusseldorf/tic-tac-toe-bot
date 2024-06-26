from bot_app import bot
from bot_app.bot_utils.general_utils.game_session_controller import GameSessionController
from bot_app.bot_utils.general_utils.render_field import RenderManager
from bot_app.bot_utils.general_utils.move_handler import MoveHandler, MoveResult
from bot_app.bot_utils.common_utils import get_name
from bot_app.bot_utils.online_utils.invite_new import InviteNew
from bot_app.bot_utils.time_out_session_controller.check_timeout import expires_session_worker
from bot_app.bot_utils.general_utils.no_session_handler import NoSessionHandler
from config.text_templates.text_tamplate_obj import template
from exceptions.session_not_exist import SessionDoesntExist
from bot_app.bot_utils.online_utils.invite_handler import InitiateInvite
from bot_app.bot_utils.online_utils.invite_sender import InviteSender
from bot_app.bot_utils.general_utils.callback_flags import CallBack
from bot_app.bot_utils.online_utils.linked_accs_session_controller import LinkedAccountsSessionController as Linkcontroller
from bot_app.bot_utils.online_utils.answer_handler import AnswerHandler


@bot.message_handler(commands=['single_game'])
def start_new_game_session(message):
    game_session = GameSessionController.start_new_session(user_one_id=message.from_user.id,
                                                           user_one_chat_id=message.chat.id,
                                                           is_online=False)
    RenderManager(game_session).render()


@bot.message_handler(commands=['online_game'])
def start_new_online_game_session(message):
    link_session_controller = Linkcontroller(message.from_user.id)
    invite = InitiateInvite(link_session_controller.get_session())
    invite.event_handle(message)


@bot.message_handler(commands=['invite_new_user'])
def invite_new_user(message):
    InviteNew.provide_user_id_to_invite(message.chat.id)


@bot.message_handler(func=lambda message: message.reply_to_message is not None)
def reply_with_id(message):
    if message.reply_to_message.from_user.id == bot.get_me().id:
        InviteNew(message.from_user.id, message.text, get_name(message.from_user.id), message.chat.id).invite()


@bot.callback_query_handler(func=lambda call: CallBack.INVT_FLAG.value in call.data)
def invite_send(call):
    linked_user, initiator_user_name, initiator_user_chat_id, _ = call.data.split()
    invite_sender = InviteSender(linked_user, initiator_user_name, initiator_user_chat_id)
    invite_sender.event_handle()


@bot.callback_query_handler(func=lambda call: CallBack.ANSWR_FLAG.value in call.data)
def answer_handler(call):
    answer, initiator_user_chat_id, linked_user_id, _ = call.data.split()
    answer_hndl = AnswerHandler(answer, initiator_user_chat_id, linked_user_id)
    if answer_hndl.handle_answer_is_agree():
        game_session = GameSessionController.start_new_session(user_one_id=initiator_user_chat_id,
                                                               user_one_chat_id=initiator_user_chat_id,
                                                               is_online=True,
                                                               user_two_id=linked_user_id,
                                                               user_two_chat_id=linked_user_id)
        RenderManager(game_session).render()


@bot.callback_query_handler(func=lambda call: CallBack.MOVE_FLAG.value in call.data)
def move_callback_handler(call):
    pos_x, pos_y, session_id, _ = call.data.split()
    session_controller = GameSessionController(session_id)

    try:
        game_session = session_controller.get_session()
    except SessionDoesntExist:
        NoSessionHandler(call.message.chat.id, call.message.message_id).inform_no_session()
        return

    move = MoveHandler(pos_x, pos_y, call.from_user.id, game_session)
    if move.make_move() is MoveResult.SUCCESS:
        RenderManager(game_session).render()


@bot.message_handler(commands=['my_id'])
def get_my_user_id(message):
    bot.send_message(message.chat.id, template.INVITING_BY_ID.INFO.format(str(message.from_user.id)))


@bot.message_handler(commands=['start', 'info'])
def introduce_bot(message):
    bot.send_message(message.chat.id, template.INTRODUCING.MESSAGE)


if __name__ == '__main__':

    expires_session_worker()
    bot.polling(non_stop=True)
