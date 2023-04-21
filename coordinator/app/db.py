from os import environ
from enum import Enum
from pymongo import MongoClient

CONNECTION_STRING = environ["MONGO_CONNECTION_STRING"]
client = MongoClient(CONNECTION_STRING)
database_name = environ["MONGO_DBNAME"]
database = client[database_name]

class Databases(Enum):
    GAMES = "GAMES"
    BOTS = "BOTS"
    PLAYERS = "PLAYERS"
    TURNS = "TURNS"
    BOARD_EVENTS = "BOARD_EVENTS"


def save_doc(db: Databases, document: dict | object) -> None:
    if not isinstance(document, dict):
        data = document.export()
    else:
        data = document
    
    database[db.value].update_one(filter={"_id": data["_id"]}, update={"$set" : data}, upsert=True)


def load_doc(db: Databases, document_id: str) -> dict:
    return database[db.value].find_one(document_id)


def get_players_in_area(window: tuple[int, int, int, int]) -> list[dict]:
    """window: x1, y1, x2, y2"""
    x1, y1, x2, y2 = window
    results = database[Databases.GAMES.value].find(
        {
            "position_x": {"$gte": x1, "$lte": x2},
            "position_y": {"$gte": y1, "$lte": y2},
        }
    )
    return [r for r in results]


def get_running_games() -> list:
    results = database[Databases.GAMES.value].find(
        {"end_time": None}
    )
    return [r for r in results]


def load_events_for_game():
    results = database[Databases.BOARD_EVENTS.value].find()
    return [r for r in results]


def load_turns_for_game():
    results = database[Databases.TURNS.value].find()
    return [r for r in results]