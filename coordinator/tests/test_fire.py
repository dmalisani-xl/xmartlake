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
PLAYER_2 = Player(
    position_x=5,
    position_y=5,
    health=100,
    fuel=50,
    bullets=10,
    shield_mounted=False,
    bot_identifier="bot2",
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
    }
    for name, v in var_default_value.items():
        if name in over.keys():
            value = over[name]
        else:
            value = v
        patch_instance.setattr(f"app.game.{name}", value)

@patch("app.game.get_players_in_area")
@patch("app.game.save_doc")
def test_player_hit_by_bullet_normal(patched_save_doc, mocked_getplayer, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    game = GAME.copy()
    mocked_getplayer.return_value = [PLAYER_2.dict()]
    bot_response = "F11NOTMATERTEXT"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "F"
    assert modified_turn.final_position_x == 7
    assert modified_turn.final_position_y == 7
    assert modified_turn.origin_bullets == 10
    assert modified_turn.final_bullets == 9
    assert modified_turn.final_health == modified_turn.origin_health
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 49
    assert modified_turn.target_reached == True
    patched_save_doc.assert_called()
    assert patched_save_doc.mock_calls[0].args == (
        Databases.PLAYERS,
        Player(position_x=5, position_y=5, fuel=50, health=80, bullets=10, shield_mounted=False, bot_identifier='bot2', owner='test', email='test@test.com', victories=0, dead=False)
    )

@patch("app.game.get_players_in_area")
@patch("app.game.save_doc")
def test_player_hit_by_bullet_shield_enemy(patched_save_doc, mocked_getplayer, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    game = GAME.copy()
    hit_player = PLAYER_2.copy()
    hit_player.shield_mounted = True
    mocked_getplayer.return_value = [hit_player.dict()]
    bot_response = "F11NOTMATERTEXT"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "F"
    assert modified_turn.final_position_x == 7
    assert modified_turn.final_position_y == 7
    assert modified_turn.origin_bullets == 10
    assert modified_turn.final_bullets == 9
    assert modified_turn.final_victories == 0
    assert modified_turn.final_health == modified_turn.origin_health
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 49
    assert modified_turn.target_reached == True
    patched_save_doc.assert_called()
    assert patched_save_doc.mock_calls[0].args == (
        Databases.PLAYERS,
        Player(position_x=5, position_y=5, fuel=50, health=90, bullets=10, shield_mounted=True, bot_identifier='bot2', owner='test', email='test@test.com', victories=0, dead=False)
    )

@patch("app.game.remove_player_from_game")
@patch("app.game.register_event")
@patch("app.game.get_players_in_area")
@patch("app.game.save_doc")
def test_player_hit_by_bullet_dead_enemy(patched_save_doc,
                                        mocked_getplayer,
                                        mocked_register_event,
                                        mocked_remove_player_from_game,
                                        monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    game = GAME.copy()
    hit_player = PLAYER_2.copy()
    hit_player.health = 10
    mocked_getplayer.return_value = [hit_player.dict()]
    bot_response = "F11NOTMATERTEXT"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "F"
    assert modified_turn.final_position_x == 7
    assert modified_turn.final_position_y == 7
    assert modified_turn.origin_bullets == 10
    assert modified_turn.final_bullets == 9
    assert modified_turn.final_victories == 1
    assert modified_turn.final_health == modified_turn.origin_health
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 49
    assert modified_turn.target_reached == True
    patched_save_doc.assert_called()
    mocked_register_event.assert_called()
    mocked_remove_player_from_game.assert_called()
    assert patched_save_doc.mock_calls[0].args == (
        Databases.PLAYERS,
        Player(position_x=5, position_y=5, fuel=50, health=0, bullets=10, shield_mounted=False, bot_identifier='bot2', owner='test', email='test@test.com', victories=0, dead=False)
    )


@patch("app.game.get_players_in_area")
@patch("app.game.save_doc")
def test_player_fire_missed(patched_save_doc, mocked_getplayer, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    game = GAME.copy()
    hit_player = PLAYER_2.copy()
    hit_player.shield_mounted = True
    mocked_getplayer.return_value = [hit_player.dict()]
    bot_response = "F22NOTMATERTEXT"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "F"
    assert modified_turn.final_position_x == 7
    assert modified_turn.final_position_y == 7
    assert modified_turn.origin_bullets == 10
    assert modified_turn.final_bullets == 9
    assert modified_turn.final_victories == 0
    assert modified_turn.final_health == modified_turn.origin_health
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 49
    assert modified_turn.target_reached == False
    patched_save_doc.assert_called()

@patch("app.game.get_players_in_area")
@patch("app.game.save_doc")
def test_player_fire_off_vision(patched_save_doc, mocked_getplayer, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    game = GAME.copy()
    hit_player = PLAYER_2.copy()
    hit_player.shield_mounted = True
    mocked_getplayer.return_value = [hit_player.dict()]
    bot_response = "F99"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "/"
    assert modified_turn.final_position_x == 7
    assert modified_turn.final_position_y == 7
    assert modified_turn.origin_bullets == 10
    assert modified_turn.final_bullets == 9
    assert modified_turn.final_victories == 0
    assert modified_turn.final_health == modified_turn.origin_health
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 49
    assert modified_turn.target_reached == False
    patched_save_doc.assert_called()


@patch("app.game.get_players_in_area")
@patch("app.game.save_doc")
def test_player_fire_out_of_bullets(patched_save_doc, mocked_getplayer, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    player.bullets = 0
    turn = TURN.copy()
    turn.origin_bullets = 0
    game = GAME.copy()
    hit_player = PLAYER_2.copy()
    hit_player.shield_mounted = True
    mocked_getplayer.return_value = [hit_player.dict()]
    bot_response = "F11"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "/"
    assert modified_turn.final_position_x == 7
    assert modified_turn.final_position_y == 7
    assert modified_turn.origin_bullets == 0
    assert modified_turn.final_bullets == 0
    assert modified_turn.final_victories == 0
    assert modified_turn.final_health == modified_turn.origin_health
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 49
    assert modified_turn.target_reached == False
    patched_save_doc.assert_called()
