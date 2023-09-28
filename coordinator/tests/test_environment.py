from pytest import MonkeyPatch
from unittest.mock import patch
from app.game import decode_environment, get_player_environment, stringfy_parameter
from app.models import Player

PLAYER_1 = Player(
    position_x=5,
    position_y=5,
    health=100,
    fuel=50,
    bullets=10,
    shield_mounted=False,
    bot_identifier="bot2",
    owner="test",
    email="test@test.com",
    victories=0,
    language="python",
    name="tested_bot1",
    code="invalid-code",
)

PLAYER_2 = Player(
    position_x=3,
    position_y=3,
    health=100,
    fuel=50,
    bullets=10,
    shield_mounted=False,
    bot_identifier="bot2",
    owner="test",
    email="test@test.com",
    victories=0,
    language="python",
    name="tested_bot2",
    code="invalid-code",
)
PLAYER_3 = Player(
    position_x=4,
    position_y=4,
    health=100,
    fuel=50,
    bullets=10,
    shield_mounted=False,
    bot_identifier="bot3",
    owner="test",
    email="test@test.com",
    victories=0,
    language="python",
    name="tested_bot1",
    code="invalid-code",
)
def _players_maker(quantity: int) -> list[Player]:
    list_of_players = []
    for x in range(quantity):
        p = Player(
            position_x=x,
            position_y=x,
            email=f"address{x}@svr.com",
            bot_identifier=f"bot{x}",
            owner="mine"
        )
        list_of_players.append(p)
    return list_of_players

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
        "current_board_width":20,
        "current_board_width": 20
    }
    for name, v in var_default_value.items():
        if name in over.keys():
            value = over[name]
        else:
            value = v
        patch_instance.setattr(f"app.game.{name}", value)

def test_decode_enviroment_with_nothing():
    ROWS = [
        ".......",
        ".......",
        ".......",
        "...X...",
        ".......",
        ".......",
        ".......",
    ]
    environment_string = "".join(ROWS) + "SOMEADDEDTEXT"
    env_dict = decode_environment(environment_string)

    assert env_dict["enemies"] == []
    assert env_dict["walls"] == []
    assert env_dict["by_coord"] == {}



def test_decode_enviroment_with_enemies():
    ROWS = [
        ".......",
        ".F.....",
        ".......",
        "...X...",
        ".......",
        ".....F.",
        ".......",
    ]
    environment_string = "".join(ROWS)
    env_dict = decode_environment(environment_string)

    assert env_dict["enemies"] == [(1, 1), (5, 5)]
    assert env_dict["walls"] == []
    assert env_dict["by_coord"] == {(1, 1): 'F', (5, 5): 'F'}


def test_decode_enviroment_with_walls():
    ROWS = [
        "WWWWWWW",
        ".......",
        ".......",
        "...X...",
        ".......",
        ".......",
        ".......",
    ]
    environment_string = "".join(ROWS)
    env_dict = decode_environment(environment_string)

    assert env_dict["enemies"] == []
    assert env_dict["walls"] == [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]
    assert env_dict["by_coord"] == {(0, 0): 'W', (1, 0): 'W', (2, 0): 'W', (3, 0): 'W', (4, 0): 'W', (5, 0): 'W', (6, 0): 'W'}

def test_decode_enviroment_with_walls_and_enemies():
    ROWS = [
        "WWWWWWW",
        ".......",
        ".......",
        "...X...",
        ".......",
        ".......",
        "......F",
    ]
    environment_string = "".join(ROWS)
    env_dict = decode_environment(environment_string)

    assert env_dict["enemies"] == [(6, 6)]
    assert env_dict["walls"] == [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]
    assert env_dict["by_coord"] == {(6, 6): 'F', (0, 0): 'W', (1, 0): 'W', (2, 0): 'W', (3, 0): 'W', (4, 0): 'W', (5, 0): 'W', (6, 0): 'W'}



def test_encode_enviroment_with_nothing():
    env = [
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'X', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.']
    ]
    player = PLAYER_1.copy()
    player.shield_mounted = False
    player.bullets = 1
    player.health = 5
    player.fuel = 9
    parameter = stringfy_parameter(player, env)
    assert parameter == '........................X........................090105F'

    player.shield_mounted = True
    player.bullets = 11
    player.health = 55
    player.fuel = 99
    parameter = stringfy_parameter(player, env)
    assert parameter == '........................X........................991155T'



def test_encode_enviroment_with_enemies():
    env = [
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'F', '.', '.', '.'],
        ['.', '.', '.', 'X', 'F', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.']
    ]
    player = PLAYER_1.copy()
    player.shield_mounted = False
    player.bullets = 1
    player.health = 5
    player.fuel = 9
    parameter = stringfy_parameter(player, env)
    assert parameter == '.................F......XF.......................090105F'


def test_encode_enviroment_with_walls():
    env = [
        ['W', '.', '.', '.', '.', '.', '.'],
        ['W', '.', '.', '.', '.', '.', '.'],
        ['W', '.', '.', 'F', '.', '.', '.'],
        ['W', '.', '.', 'X', 'F', '.', '.'],
        ['W', '.', '.', '.', '.', '.', '.'],
        ['W', '.', '.', '.', '.', '.', '.'],
        ['W', '.', '.', '.', '.', '.', '.']
    ]
    player = PLAYER_1.copy()
    player.shield_mounted = False
    player.bullets = 1
    player.health = 5
    player.fuel = 9
    parameter = stringfy_parameter(player, env)
    assert parameter == 'W......W......W..F...W..XF..W......W......W......090105F'

@patch("app.game.get_players_in_environment", return_value=[])
def test_get_player_environment_with_nothing(mk_get_players, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    env = get_player_environment(player)
    assert env == [
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'X', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.']
    ]

@patch("app.game.get_players_in_environment", return_value=[])
def test_get_player_environment_wall_on_left(mk_get_players, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    player.position_x = 2
    env = get_player_environment(player)
    assert env == [
        ['W', '.', '.', '.', '.', '.', '.'],
        ['W', '.', '.', '.', '.', '.', '.'],
        ['W', '.', '.', '.', '.', '.', '.'],
        ['W', '.', '.', 'X', '.', '.', '.'],
        ['W', '.', '.', '.', '.', '.', '.'],
        ['W', '.', '.', '.', '.', '.', '.'],
        ['W', '.', '.', '.', '.', '.', '.']
    ]


@patch("app.game.get_players_in_environment", return_value=[])
def test_get_player_environment_wall_on_right(mk_get_players, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    player.position_x = 17
    env = get_player_environment(player)
    assert env == [
        ['.', '.', '.', '.', '.', '.', 'W'],
        ['.', '.', '.', '.', '.', '.', 'W'],
        ['.', '.', '.', '.', '.', '.', 'W'],
        ['.', '.', '.', 'X', '.', '.', 'W'],
        ['.', '.', '.', '.', '.', '.', 'W'],
        ['.', '.', '.', '.', '.', '.', 'W'],
        ['.', '.', '.', '.', '.', '.', 'W']
    ]

@patch("app.game.get_players_in_environment", return_value=[])
def test_get_player_environment_wall_on_right_at_limit(mk_get_players, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    player.position_x = 19
    env = get_player_environment(player)
    assert env == [
        ['.', '.', '.', '.', 'W', 'W', 'W'],
        ['.', '.', '.', '.', 'W', 'W', 'W'],
        ['.', '.', '.', '.', 'W', 'W', 'W'],
        ['.', '.', '.', 'X', 'W', 'W', 'W'],
        ['.', '.', '.', '.', 'W', 'W', 'W'],
        ['.', '.', '.', '.', 'W', 'W', 'W'],
        ['.', '.', '.', '.', 'W', 'W', 'W']
    ]

@patch("app.game.get_players_in_environment", return_value=[])
def test_get_player_environment_wall_on_up(mk_get_players, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    player.position_y = 2
    env = get_player_environment(player)
    assert env == [
        ['W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'X', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.']
    ]

@patch("app.game.get_players_in_environment", return_value=[])
def test_get_player_environment_wall_on_up_at_limit(mk_get_players, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    player.position_y = 0
    env = get_player_environment(player)
    assert env == [
        ['W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ['W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ['W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ['.', '.', '.', 'X', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.']
    ]

@patch("app.game.get_players_in_environment", return_value=[])
def test_get_player_environment_wall_on_down(mk_get_players, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    player.position_y = 17
    env = get_player_environment(player)
    assert env == [
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'X', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['W', 'W', 'W', 'W', 'W', 'W', 'W']
    ]


@patch("app.game.get_players_in_environment", return_value=[])
def test_get_player_environment_wall_on_down_at_limit(mk_get_players, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    player.position_y = 19
    env = get_player_environment(player)
    assert env == [
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'X', '.', '.', '.'],
        ['W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ['W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ['W', 'W', 'W', 'W', 'W', 'W', 'W']
    ]

@patch("app.game.get_players_in_environment", return_value=[])
def test_get_player_environment_wall_on_right_down_corner(mk_get_players, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    player.position_y = 19
    player.position_x = 19
    env = get_player_environment(player)
    assert env == [
        ['.', '.', '.', '.', 'W', 'W', 'W'],
        ['.', '.', '.', '.', 'W', 'W', 'W'],
        ['.', '.', '.', '.', 'W', 'W', 'W'],
        ['.', '.', '.', 'X', 'W', 'W', 'W'],
        ['W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ['W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ['W', 'W', 'W', 'W', 'W', 'W', 'W']
    ]


@patch("app.game.get_players_in_environment", return_value=[])
def test_get_player_environment_wall_on_upper_left_corner(mk_get_players, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    player.position_y = 0
    player.position_x = 0
    env = get_player_environment(player)
    assert env == [
        ['W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ['W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ['W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ['W', 'W', 'W', 'X', '.', '.', '.'],
        ['W', 'W', 'W', '.', '.', '.', '.'],
        ['W', 'W', 'W', '.', '.', '.', '.'],
        ['W', 'W', 'W', '.', '.', '.', '.']
    ]

@patch("app.game.get_players_in_environment", return_value=[])
def test_get_player_environment_wall_close_to_upper_left_corner(mk_get_players, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    player.position_y = 2
    player.position_x = 2
    env = get_player_environment(player)
    assert env == [
        ['W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ['W', '.', '.', '.', '.', '.', '.'],
        ['W', '.', '.', '.', '.', '.', '.'],
        ['W', '.', '.', 'X', '.', '.', '.'],
        ['W', '.', '.', '.', '.', '.', '.'],
        ['W', '.', '.', '.', '.', '.', '.'],
        ['W', '.', '.', '.', '.', '.', '.']
    ]

@patch("app.game.get_players_in_environment", return_value=[PLAYER_2, PLAYER_3])
def test_get_player_environment_with_enemies_and_walls(mk_get_players, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    player.position_y = 2
    player.position_x = 2
    env = get_player_environment(player)
    assert env == [
        ['W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ['W', '.', '.', '.', '.', '.', '.'],
        ['W', '.', '.', '.', '.', '.', '.'],
        ['W', '.', '.', 'X', '.', '.', '.'],
        ['W', '.', '.', '.', 'F', '.', '.'],
        ['W', '.', '.', '.', '.', 'F', '.'],
        ['W', '.', '.', '.', '.', '.', '.']
    ]

@patch("app.game.get_players_in_environment", return_value=[PLAYER_2, PLAYER_3])
def test_get_player_environment_with_enemies_only(mk_get_players, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    player = PLAYER_1.copy()
    player.position_x = 3
    player.position_y = 4
    env = get_player_environment(player)

    assert env == [
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'F', '.', '.', '.'],
        ['.', '.', '.', 'X', 'F', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.']
    ]