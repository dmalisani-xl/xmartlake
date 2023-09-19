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

def uuid4_generator() -> str:
    return str(uuid4())

class SupportedLanguage(str, Enum):
    python = 'python'
    nodejs = 'nodejs/javascript'

class GameEventType(Enum):
    START_GAME = "START_GAME"
    END_GAME = "END_GAME"
    END_ROUND = "END_ROUND"
    SOME_DIED = "SOME_DIED"
    COLLISION = "COLLISION"


class ActionOfBot(Enum):
    FIRE = "F"
    MOVE = "M"
    SHIELD = "S"
    REFUEL = "R"
    LOAD = "L"  # Load bullets
    TOOLS = "T"  # Repair turn
    SKIPPED = "/"


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
    dead: bool = False

    @property
    def _id(self) -> str:
        return self.bot_identifier

    def export(self) -> dict:
        data = self.dict()
        data["_id"] = self._id
        return data

class PlayerLoader(BaseModel):
    bot_identifier: str = Field(default_factory=uuid4_generator)
    language: SupportedLanguage
    name: str
    email: EmailStr
    code: str
    avatar_b64: str
    creation_datetime: datetime = datetime.now()
    built: bool = False
    image_identifier: str

    class Config:
        fields = {"built": {"exclude": True}, "image_identifier": {"exclude": True}}

        schema_extra = {
            "example": {
                "language": "python",
                "name": "John Doe",
                "email": "johndoe@example.com",
                "code": "<base64-encoded-function>",
                "avatar_b64": "<base64-encoded-string>",
            }
        }

    @validator("avatar_b64")
    def png_or_jpg_length_less_than_64k(cls, v):
        if len(v) > 64000:
            raise ValidationError("Avatar is too big", model=PlayerLoader)
        if not v.startswith("data:image/jpeg;base64,") or v.startswith("data:image/png;base64,"):
            raise ValidationError("Avatar must have a PNG or JPG", model=PlayerLoader)
        return v


class TurnRecord(BaseModel):
    turn_identifier: str = Field(default_factory=uuid4_generator)
    timestamp: datetime = Field(default_factory=datetime.now)
    session_identifier: str
    bot_identifier: str
    turn_number: int

    origin_position_x: int
    origin_position_y: int
    origin_fuel: int
    origin_health: int
    origin_bullets: int
    origin_victories: int
    origin_shield_enabled: bool = False

    final_position_x: int | None = None
    final_position_y: int | None = None
    final_fuel: int | None = None
    final_health: int | None = None
    final_bullets: int | None = None
    final_victories: int | None = None
    final_shield_enabled: bool | None = None

    sent_payload: str
    received_response: str | None = None
    action: str | None = None
    dead: bool = False
    collision: bool = False
    collision_to: bool = False
    hit: bool = False  # by collision
    hit_to: str | None = None 
    target_reached: bool = False
    target_abs_coordinates: str = ""
    wrong_response: bool = False
    notes: str = ""

    @property
    def _id(self) -> str:
        return self.turn_identifier

    def export(self) -> dict:
        data = self.dict()
        data["_id"] = self._id
        return data

class GameSession(BaseModel):
    session_identifier: str = Field(default_factory=uuid4_generator)
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: datetime | None = None
    initial_players: set[str]
    current_players: set[str]
    players_order: list[str]
    last_bot_played: str | None
    current_turn: int = 0
    past_turns: list[str] = []
    board_size_x: int = DEFAULT_WIDTH
    board_size_y: int = DEFAULT_HEIGHT
    winner: str | None = None
    players_position: list[list[str]] | None = None
    normal_size_limit: int
    stop_limit: int = DEFAULT_STOP_LIMIT

    @property
    def _id(self) -> str:
        return self.session_identifier
    
    def export(self) -> dict:
        data = self.dict()
        data["_id"] = self._id
        data["initial_players"] = list(self.initial_players)
        data["current_players"] = list(self.current_players)
        return data

class GameEvent(BaseModel):
    event_type: GameEventType
    session_identifier: str
    timestamp: datetime = Field(default_factory=datetime.now)
    aditional_info: str | None

    def export(self) -> dict:
        data = self.dict()
        data["_id"] = str(uuid4())
        data["event_type"] = self.event_type.value
        return data