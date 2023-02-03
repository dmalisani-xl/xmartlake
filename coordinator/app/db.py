from enum import Enum

class Databases(Enum):
    GAMES = "GAMES"
    BOTS = "BOTS"
    PLAYERS = "PLAYERS"
    TURNS = "TURNS"
    BOARD_EVENTS = "BOARD_EVENTS"


def save_doc(db: Databases, document) -> None:
    raise NotImplementedError

def get_players_in_area(window: tuple[int, int, int, int]) -> list[dict]:
    """window: x1, y1, x2, y2"""
    raise NotImplementedError
