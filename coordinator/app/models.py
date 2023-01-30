from pydantic import (
    BaseModel,
    EmailStr,
    ValidationError,
    validator,
    PrivateAttr,
    Field
)
from enum import Enum
from datetime import datetime
from uuid import uuid4

from app.settings import (
    DEFAULT_FUEL,
    DEFAULT_HEALTH,
    DEFAULT_BULLETS,
    DEFAULT_WIDTH,
    DEFAULT_HEIGHT,
    DEFAULT_STOP_LIMIT
)

class SupportedLanguage(str, Enum):
    python = 'python'
    nodejs = 'nodejs/javascript'

class GameEventType(Enum):
    START_GAME = "START_GAME"
    END_GAME = "END_GAME"
    END_ROUND = "END_ROUND"
    SOME_DIED = "SOME_DIED"


class ActionOfBot(Enum):
    FIRE = "F"
    MOVE = "M"
    SHIELD = "S"
    REFUEL = "R"
    LOAD = "L"  # Load bullets
    TOOLS = "T"  # Repair turn


class Player(BaseModel):
    position_x: int
    position_y: int
    fuel: int = DEFAULT_FUEL
    health: int = DEFAULT_HEALTH
    bullets: int = DEFAULT_BULLETS
    shield_mounted: bool = False
    bot_identifier: str
    owner: str
    email: EmailStr
    victories: int = 0



class PlayerLoader(BaseModel):
    bot_identifier: str = Field(default_factory=uuid4)
    language: SupportedLanguage
    name: str
    email: EmailStr
    code: str
    avatar_b64: str
    _datetime: datetime = PrivateAttr(default_factory=datetime.now)
    _built: bool = False

    @validator("avatar_b64")
    def png_or_jpg_length_less_than_64k(cls, value):
        if len(value) > 64000:
            raise ValidationError("Avatar is too big")
        if not value.startswith("data:image/jpeg;base64,") or value.startswith("data:image/png;base64,"):
            raise ValidationError("Avatar must have a PNG or JPG")
        return value


class TurnRecord(BaseModel):
    turn_identifier: str = Field(default_factory=uuid4)
    datetime: datetime
    bot_identifier: str
    turn_number: int

    origin_position_x: int
    origin_position_y: int
    origin_fuel: int
    origin_health: int
    origin_bullets: int
    origin_victories: int

    final_position_x: int
    final_position_y: int
    final_fuel: int
    final_health: int
    final_bullets: int
    final_victories: int

    sent_payload: str
    received_response: str
    action: ActionOfBot
    dead: bool = False


class GameSession(BaseModel):
    session_identifier: str = Field(default_factory=uuid4)
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: datetime | None = None
    initial_players: set[str]
    current_players: set[str]
    players_order: list[str]
    current_turn: str | None = None
    past_turns: list[str] = []
    board_size_x: int = DEFAULT_WIDTH
    board_size_y: int = DEFAULT_HEIGHT
    winner: str | None = None
    players_position: list[list[str]] | None = None
    normal_size_limit: int
    stop_limit: int = DEFAULT_STOP_LIMIT
    

class GameEvent(BaseModel):
    event_type: GameEventType
    session_identifier: str
    _datetime: datetime = PrivateAttr(default_factory=datetime.now)
    aditional_info: str | None
