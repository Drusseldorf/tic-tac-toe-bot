from telebot.apihelper import ApiTelegramException

from bot_app import bot


def get_name(user_id: str):
    try:
        chat_info = bot.get_chat(user_id)
    except ApiTelegramException:
        print('ApiTelegramException get_name')
        return f'ID: {user_id}'

    return chat_info.first_name if chat_info.first_name else chat_info.username


