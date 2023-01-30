from enum import Enum

class Databases(Enum):
    GAMES = "GAMES"
    BOTS = "BOTS"
    PLAYERS = "PLAYERS"
    TURNS = "TURNS"
    BOARD_EVENTS = "BOARD_EVENTS"


def save_doc(db: Databases, document) -> None:
    raise NotImplementedError