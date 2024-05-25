from enum import Enum


class CallBack(Enum):
    MOVE_FLAG = 'MOVE'
    INVT_FLAG = 'INVT'
    ANSWR_FLAG = 'ANSWR'


class Answer(Enum):
    AGREE = 'AGREE'
    DISAGREE = 'DISAGREE'
