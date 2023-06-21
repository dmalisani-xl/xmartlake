from unittest.mock import patch
from pytest import MonkeyPatch

from app.models import Player, GameSession, TurnRecord
from pytest import MonkeyPatch
from app.game import process_response_of_player
from app.db import  Databases
from app.settings import *


GAME =  GameSession(
        initial_players={"bot1", "bot2", "bot3"},
        current_players={"bot1", "bot2", "bot3"},
        players_order=["bot1", "bot2", "bot3"],
        normal_size_limit=10,
        board_size_x=15,
        board_size_y=15
    )

PLAYER_1 = Player(
    position_x=7,
    position_y=7,
    health=100,
    fuel=50,
    bullets=10,
    shield_mounted=False,
    bot_identifier="bot1",
    owner="test",
    email="test@test.com",
    victories=0
)


ROWS = [
    ".......",
    ".F.....",
    ".......",
    "...X...",
    ".......",
    ".......",
    ".......",
]
PAYLOAD = "".join(ROWS)

TURN = TurnRecord(
    bot_identifier="bot1",
    turn_number=1,
    session_identifier="game_id",
    origin_position_x=PLAYER_1.position_x,
    origin_position_y=PLAYER_1.position_y,
    origin_bullets=PLAYER_1.bullets,
    origin_fuel=PLAYER_1.fuel,
    origin_health=PLAYER_1.health,
    origin_shield_enabled=PLAYER_1.shield_mounted,
    origin_victories=0,
    sent_payload=PAYLOAD
)


def patch_settings(patch_instance, overwrite: dict = None):
    over = overwrite if overwrite else {}
    var_default_value = {
        "DEFAULT_VISIBILY_DISTANCE": 3,
        "PLAYER_POSITION_IDENTIFICACION": "X",
        "DEFAULT_EMPTY_PLACE_SYMBOL": ".",
        "FOE_SYMBOL": "F",
        "WALL_SYMBOL": "W",
        "DEFAULT_WIDTH": 20,
        "DEFAULT_HEIGHT": 20,
        "DAMAGE_BY_BULLET": 20,
        "FUEL_CONSUMED_BY_TURN": 1,
        "FUEL_CONSUMED_BY_TURN_WITH_SHIELD": 2,
        "REFUEL_BY_TURN": 15
    }
    for name, v in var_default_value.items():
        if name in over.keys():
            value = over[name]
        else:
            value = v
        patch_instance.setattr(f"app.game.{name}", value)


@patch("app.game.save_doc")
def test_player_reload_fuel_normal(patched_save_doc, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    game = GAME.copy()

    bot_response = "R99999"  # Only matter the first character
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "R"
    assert modified_turn.final_position_x == 7
    assert modified_turn.final_position_y == 7
    assert modified_turn.origin_bullets == 10
    assert modified_turn.final_bullets == 10
    assert modified_turn.final_health == modified_turn.origin_health
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.origin_fuel == 50
    assert modified_turn.final_fuel == 64
    assert modified_turn.target_reached == False
    patched_save_doc.assert_called()


@patch("app.game.save_doc")
def test_player_reload_fuel_with_shield(patched_save_doc, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    player.shield_mounted = True
    turn = TURN.copy()
    turn.origin_shield_enabled = True
    game = GAME.copy()

    bot_response = "R99999"  # Only matter the first character
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "R"
    assert modified_turn.final_position_x == 7
    assert modified_turn.final_position_y == 7
    assert modified_turn.origin_bullets == 10
    assert modified_turn.final_bullets == 10
    assert modified_turn.final_health == modified_turn.origin_health
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.origin_fuel == 50
    assert modified_turn.final_fuel == 63
    assert modified_turn.target_reached == False
    patched_save_doc.assert_called()
