from copy import copy
from unittest.mock import patch
from pytest import MonkeyPatch

from app.models import Player, GameSession, TurnRecord
from pytest import MonkeyPatch
from app.game import process_response_of_player

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
    var_default_value = [
        ("FUEL_CONSUMED_BY_TURN", 1),
        ("FUEL_CONSUMED_BY_TURN_WITH_SHIELD",  2),
        ("DEFAULT_VISIBILY_DISTANCE", 3),
        ("DAMAGE_BY_HIT", 10),
        ("SHIELD_PROTECTION_PERCENTAGE", 50),
        ("DEFAULT_WIDTH", 100),
        ("DEFAULT_HEIGHT", 100),
    ]
    for name, v in var_default_value:
        if name in over.keys():
            value = over[name]
        else:
            value = v
        patch_instance.setattr(f"app.game.{name}", value)

@patch("app.game.save_doc")
def test_move_single_step_down_right(patched_save_doc, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    game = GAME.copy()
    bot_response = "M44NOTMATERTEXT"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "M"
    assert modified_turn.final_position_x == 8
    assert modified_turn.final_position_y == 8
    assert modified_turn.final_bullets == modified_turn.origin_bullets
    assert modified_turn.final_health == modified_turn.origin_health
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 48
    patched_save_doc.assert_called()


@patch("app.game.save_doc")
def test_move_single_step_up(patched_save_doc, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    game = GAME.copy()
    bot_response = "M32NOTMATERTEXT"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "M"
    assert modified_turn.final_position_x == 7
    assert modified_turn.final_position_y == 6
    assert modified_turn.final_bullets == modified_turn.origin_bullets
    assert modified_turn.final_health == modified_turn.origin_health
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 49
    patched_save_doc.assert_called()


@patch("app.game.save_doc")
def test_move_single_double_step_up(patched_save_doc, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    game = GAME.copy()
    bot_response = "M31NOTMATERTEXT"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "M"
    assert modified_turn.final_position_x == 7
    assert modified_turn.final_position_y == 5
    assert modified_turn.final_bullets == modified_turn.origin_bullets
    assert modified_turn.final_health == modified_turn.origin_health
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 48
    patched_save_doc.assert_called()


@patch("app.game.save_doc")
def test_move_single_double_step_up_left(patched_save_doc, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    game = GAME.copy()
    bot_response = "M21NOTMATERTEXT"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "M"
    assert modified_turn.final_position_x == 6
    assert modified_turn.final_position_y == 5
    assert modified_turn.final_bullets == modified_turn.origin_bullets
    assert modified_turn.final_health == modified_turn.origin_health
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 46
    patched_save_doc.assert_called()

@patch("app.game.save_doc")
def test_move_single_double_step_up_left_corner(patched_save_doc, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    game = GAME.copy()
    bot_response = "M00NOTMATERTEXT"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "M"
    assert modified_turn.final_position_x == 4
    assert modified_turn.final_position_y == 4
    assert modified_turn.final_bullets == modified_turn.origin_bullets
    assert modified_turn.final_health == modified_turn.origin_health
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 18
    patched_save_doc.assert_called()


@patch("app.game.save_doc")
def test_move_single_double_step_down_right_corner(patched_save_doc, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    game = GAME.copy()
    bot_response = "M66NOTMATERTEXT"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "M"
    assert modified_turn.final_position_x == 10
    assert modified_turn.final_position_y == 10
    assert modified_turn.final_bullets == modified_turn.origin_bullets
    assert modified_turn.final_health == modified_turn.origin_health
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 18
    patched_save_doc.assert_called()

@patch("app.game.save_doc")
def test_move_stand(patched_save_doc, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    game = GAME.copy()
    bot_response = "M33NOTMATERTEXT"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "M"
    assert modified_turn.final_position_x == 7
    assert modified_turn.final_position_y == 7
    assert modified_turn.final_bullets == modified_turn.origin_bullets
    assert modified_turn.final_health == modified_turn.origin_health
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 49
    patched_save_doc.assert_called()

@patch("app.game.save_doc")
def test_move_stand_with_consumed_change(patched_save_doc, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch, {"FUEL_CONSUMED_BY_TURN": 5})
    player = PLAYER_1.copy()
    turn = TURN.copy()
    game = GAME.copy()
    bot_response = "M33NOTMATERTEXT"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "M"
    assert modified_turn.final_position_x == 7
    assert modified_turn.final_position_y == 7
    assert modified_turn.final_bullets == modified_turn.origin_bullets
    assert modified_turn.final_health == modified_turn.origin_health
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 45
    patched_save_doc.assert_called()

@patch("app.game.save_doc")
def test_move_stand_with_shield(patched_save_doc, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    turn.origin_shield_enabled = True
    game = GAME.copy()
    bot_response = "M33NOTMATERTEXT"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "M"
    assert modified_turn.final_position_x == 7
    assert modified_turn.final_position_y == 7
    assert modified_turn.final_bullets == modified_turn.origin_bullets
    assert modified_turn.final_health == modified_turn.origin_health
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 48
    patched_save_doc.assert_called()


@patch("app.game.save_doc")
def test_move_double_with_shield(patched_save_doc, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    turn.origin_shield_enabled = True
    game = GAME.copy()
    bot_response = "M31NOTMATERTEXT"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "M"
    assert modified_turn.final_position_x == 7
    assert modified_turn.final_position_y == 5
    assert modified_turn.final_bullets == modified_turn.origin_bullets
    assert modified_turn.final_health == modified_turn.origin_health
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 46
    patched_save_doc.assert_called()


@patch("app.game.save_doc")
def test_move_outside_of_visibility(patched_save_doc, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    game = GAME.copy()
    bot_response = "M99NOTMATERTEXT"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "/"
    assert modified_turn.final_position_x == 7
    assert modified_turn.final_position_y == 7
    assert modified_turn.final_bullets == modified_turn.origin_bullets
    assert modified_turn.final_health == modified_turn.origin_health
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 49
    patched_save_doc.assert_called()

@patch("app.game.get_players_in_area")
@patch("app.game.save_doc")
def test_move_to_collision(patched_save_doc, mocked_getplayer, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    game = GAME.copy()
    mocked_getplayer.return_value = PLAYER_2.dict()
    bot_response = "M11NOTMATERTEXT"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "M"
    assert modified_turn.final_position_x == 6
    assert modified_turn.final_position_y == 5
    assert modified_turn.hit
    assert modified_turn.final_bullets == modified_turn.origin_bullets
    assert modified_turn.final_health == 90
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 42
    call_to_player_record = patched_save_doc.call_args_list[0].args
    assert call_to_player_record[0].value == "PLAYERS"
    hit_player = call_to_player_record[1]
    assert hit_player.health == 90

@patch("app.game.get_players_in_area")
@patch("app.game.save_doc")
def test_move_to_collision_with_shield(patched_save_doc, mocked_getplayer, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    game = GAME.copy()
    mocked_getplayer.return_value = PLAYER_2.dict()
    bot_response = "M11NOTMATERTEXT"
    turn.origin_shield_enabled = True
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "M"
    assert modified_turn.final_position_x == 6
    assert modified_turn.final_position_y == 5
    assert modified_turn.hit
    assert modified_turn.final_bullets == modified_turn.origin_bullets
    assert modified_turn.final_health == 95
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 23
    call_to_player_record = patched_save_doc.call_args_list[0].args
    assert call_to_player_record[0].value == "PLAYERS"
    hit_player = call_to_player_record[1]
    assert hit_player.health == 90

@patch("app.game.get_players_in_area")
@patch("app.game.save_doc")
def test_move_to_collision_with_enemy_shield(patched_save_doc, mocked_getplayer, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    player2 = PLAYER_2.copy()
    player2.shield_mounted = True
    turn = TURN.copy()
    game = GAME.copy()
    mocked_getplayer.return_value = player2.dict()
    bot_response = "M11NOTMATERTEXT"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "M"
    assert modified_turn.final_position_x == 6
    assert modified_turn.final_position_y == 5
    assert modified_turn.hit
    assert modified_turn.final_bullets == modified_turn.origin_bullets
    assert modified_turn.final_health == 90
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 42
    call_to_player_record = patched_save_doc.call_args_list[0].args
    assert call_to_player_record[0].value == "PLAYERS"
    hit_player = call_to_player_record[1]
    assert hit_player.health == 95


@patch("app.game.get_players_in_area")
@patch("app.game.save_doc")
def test_move_to_collision_with_both_shield(patched_save_doc, mocked_getplayer, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    player2 = PLAYER_2.copy()
    player2.shield_mounted = True
    turn = TURN.copy()
    game = GAME.copy()
    turn.origin_shield_enabled = True
    mocked_getplayer.return_value = player2.dict()
    bot_response = "M11NOTMATERTEXT"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "M"
    assert modified_turn.final_position_x == 6
    assert modified_turn.final_position_y == 5
    assert modified_turn.hit
    assert modified_turn.final_bullets == modified_turn.origin_bullets
    assert modified_turn.final_health == 95
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 23
    call_to_player_record = patched_save_doc.call_args_list[0].args
    assert call_to_player_record[0].value == "PLAYERS"
    hit_player = call_to_player_record[1]
    assert hit_player.health == 95


@patch("app.game.save_doc")
def test_move_outside_of_limits(patched_save_doc, monkeypatch: MonkeyPatch):
    patch_settings(
        monkeypatch,
        {"DEFAULT_WIDTH": 8, "DEFAULT_HEIGHT": 8}
    )
    player = PLAYER_1.copy()
    turn = TURN.copy()
    game = GAME.copy()
    bot_response = "M99NOTMATERTEXT"
    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "/"
    assert modified_turn.final_position_x == 7
    assert modified_turn.final_position_y == 7
    assert modified_turn.final_bullets == modified_turn.origin_bullets
    assert modified_turn.final_health == modified_turn.origin_health
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 49
    patched_save_doc.assert_called()


@patch("app.game.save_doc")
def test_move_to_wall_collision(patched_save_doc, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    ROWS = [
        "WWWWWWW",
        "WWWWWWW",
        "......W",
        "...X..W",
        "......W",
        "......W",
        "......W",
    ]
    turn.sent_payload = "".join(ROWS)
    game = GAME.copy()
    bot_response = "M11NOTMATERTEXT"

    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "M"
    assert modified_turn.final_position_x == 7
    assert modified_turn.final_position_y == 6
    assert modified_turn.hit
    assert modified_turn.final_bullets == modified_turn.origin_bullets
    assert modified_turn.final_health == 90
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 42

@patch("app.game.dump_turn_to_botstatus")
@patch("app.game.save_doc")
def test_move_to_wall_collision_with_shield(patched_save_doc, mocked_savestatus, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    ROWS = [
        "WWWWWWW",
        "WWWWWWW",
        "......W",
        "...X..W",
        "......W",
        "......W",
        "......W",
    ]
    turn.sent_payload = "".join(ROWS)
    turn.origin_shield_enabled = True
    game = GAME.copy()
    bot_response = "M11NOTMATERTEXT"

    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "M"
    assert modified_turn.final_position_x == 7
    assert modified_turn.final_position_y == 6
    assert modified_turn.hit
    assert modified_turn.final_bullets == modified_turn.origin_bullets
    assert modified_turn.final_health == 95
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 23
    mocked_savestatus.called_once()

@patch("app.game.dump_turn_to_botstatus")
@patch("app.game.get_players_in_area")
@patch("app.game.save_doc")
def test_move_to_collision_all_path_occupied(
    patched_save_doc,
    mocked_getplayer,
    mocked_savestatus,
    monkeypatch: MonkeyPatch
):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    turn = TURN.copy()
    mocked_getplayer.return_value = PLAYER_2.dict()
    ROWS = [
        "...F..W",
        "...F..W",
        "...F..W",
        "...X..W",
        "......W",
        "......W",
        "......W",
    ]
    turn.sent_payload = "".join(ROWS)
    game = GAME.copy()
    bot_response = "M31NOTMATERTEXT"

    turn.received_response = bot_response
    modified_turn = process_response_of_player(game=game, player=player, turn=turn)
    assert modified_turn.action == "M"
    assert modified_turn.final_position_x == 7
    assert modified_turn.final_position_y == 7
    assert modified_turn.hit
    assert modified_turn.final_bullets == modified_turn.origin_bullets
    assert modified_turn.final_health == 90
    assert modified_turn.final_shield_enabled == modified_turn.origin_shield_enabled
    assert modified_turn.final_fuel == 48
    mocked_savestatus.called_once()


# test target death
# test source death