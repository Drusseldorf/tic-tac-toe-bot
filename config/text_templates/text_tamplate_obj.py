from pathlib import Path
from pydantic import BaseModel
from pydantic_settings_yaml import YamlBaseSettings
import warnings

warnings.filterwarnings('ignore')

TEXTS_PATH = Path(__file__).parent.joinpath('text_templates.yaml')


class MoveTurnText(BaseModel):
    NEXT_TURN: str
    WON: str
    DRAW: str


class MoveTurnTextOnline(BaseModel):
    NEXT_TURN: str
    WON: str
    DRAW: str


class NoSessionText(BaseModel):
    INFORM_MESSAGE: str


class InviteEventText(BaseModel):
    INVITE_MESSAGE: str
    CHOOSE_USER_MESSAGE: str
    NO_LINKED_USERS_YET: str
    AGREE: str
    DISAGREE: str
    INVITE_WAS_SENT_SUCCESSFULLY: str
    INVITE_WAS_SENT_UNSUCCESSFULLY: str


class InviteAnswerText(BaseModel):
    INVITED_USER_DISAGREE: str
    INVITED_USER_AGREE: str
    INITIATOR_USER_DISAGREE: str
    INITIATOR_USER_AGREE: str


class InvitingById(BaseModel):
    INFO: str
    UNKOWN_USER: str
    GIVE_ME_USER_ID: str
    INVITING_HIMSELF: str


class Introducing(BaseModel):
    MESSAGE: str


class Templates(YamlBaseSettings):
    MOVE_TURN_TEXT: MoveTurnText
    MOVE_TURN_TEXT_ONLINE: MoveTurnTextOnline
    NO_SESSION_TEXT: NoSessionText
    INVITE_EVENT_TEXT: InviteEventText
    INVITE_ANSWER_TEXT: InviteAnswerText
    INVITING_BY_ID: InvitingById
    INTRODUCING: Introducing

    class Config:
        yaml_file = TEXTS_PATH


template = Templates()
