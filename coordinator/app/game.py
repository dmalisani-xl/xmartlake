from random import shuffle

from app.settings import NORMAL_SIZE_LIMIT
from app.db import save_doc, Databases
from app.models import Player, GameSession, GameEvent


def start_new_game(*,
                   players:list[Player],
                   width: int,
                   height: int) -> tuple[GameSession, bool]:
    current_game = load_ongoing_game()
    if current_game:
        return current_game, True

    players_id = {pyr.bot_identifier for pyr in players}
    list_players = list(players_id)
    shuffle(list_players)

    session = GameSession(
        initial_players=players_id,
        current_players=players_id,
        players_order=list_players,
        normal_size_limit=NORMAL_SIZE_LIMIT
    )
    save_doc(Databases.GAMES, session)
    return session

def load_ongoing_game() -> None | GameSession:
    """Return the ongoing game if exists"""

def _choice_next_player(session: GameSession) -> Player:
    ...

def _load_player(bot_id: str) -> Player:
    ...

def get_player_environment(Player) -> list(list[str]):
    ...

def stringfy_parameter(player: Player, environment: list[list[str]]):
    ...

def call_to_bot(player: Player, parameter: str) -> str:
    ...

def play_next_turn(session: GameSession) -> str:
    player_id = _choice_next_player(session)
    player = _load_player(player_id)
    environment = get_player_environment
    turn_parameter = stringfy_parameter(player, environment)
    response = call_to_bot(player, turn_parameter)
    return response

def _get_all_players() -> list[Player]:
    ...

def _randomize_positions(players: list[Player]):
    # Need detect overlaping
    # Save positions to db
    ...

def execute_loop(game: Player) -> Player:
    ...

def get_events(game: GameSession) -> list[GameEvent]:
    ...

def play() -> Player:  # return winner
    all_players = _get_all_players()
    game, ongoing = start_new_game(players = all_players, width=100, height=100)
    if not ongoing:
        _randomize_positions(all_players)
    winner = execute_loop(game)
    events = get_events(game)
    return {"winner": winner, "events": events}
