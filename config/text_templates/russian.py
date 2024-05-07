class MoveTurnText:

    NEXT_TURN = 'Ходят'
    WON = 'Победили'
    DRAW = 'Ничья'


class MoveTurnTextOnline:

    NEXT_TURN = 'Ходит {}'
    WON = 'Победил игрок {}'
    DRAW = 'Ничья'


class NoSessionText:

    INFORM_MESSAGE = 'Похоже, что игра закончена или время сессии истекло :(\n' \
                     'Вы можете начать новую игру: /single_game'


class InviteEventText:

    INVITE_MESSAGE = 'Привет! {} бросает тебе вызов в крестики-нолики'
    CHOOSE_USER_MESSAGE = 'Выбери соперника из списка\n' \
                          'Чтобы пригласить нового: /invite_new_user'
    NO_LINKED_USERS_YET = 'У тебя еще нет связанного списка игроков\n' \
                          'Чтобы пригласить нового пользователя воспользуся командой /invite_new_user'
    AGREE = 'Начнем!'
    DISAGREE = 'Не сейчас :('
    INVITE_WAS_SENT_SUCCESSFULLY = 'Приглашение для {} успешно отправлено\n' \
                                   'Ожидаем ответа'
    INVITE_WAS_SENT_UNSUCCESSFULLY = 'Не удалось отправить приглашение для {}\n' \
                                     'Попробуйте пригласить этого игрока позже или пригласите другого игрока'


class InviteAnswerText:

    INVITED_USER_DISAGREE = 'Значит в следующий раз'
    INVITED_USER_AGREE = 'Отлично!'
    INITIATOR_USER_DISAGREE = '{} не хочет сейчас играть :('
    INITIATOR_USER_AGREE = '{} согласился!'
