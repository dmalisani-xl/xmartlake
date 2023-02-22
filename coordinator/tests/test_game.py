import pytest
from unittest.mock import patch, Mock

from app.models import Player, GameSession, TurnRecord
from app.game import start_new_game, process_response_of_player


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


@patch("app.game.save_doc")
def test_gamestarter(patched_save_doc):
    players = _players_maker(5)
    game, _ = start_new_game(players=players, width=100, height=200)
    assert type(game) == GameSession
    assert set(game.current_players) == set(game.initial_players)
    assert len(game.initial_players) == len(game.players_order)
    patched_save_doc.assert_called_once()


base_game = GameSession(
            board_size_x=100,
            board_size_y=100,
            initial_players={"a", "b"},
            current_players={"a", "b"},
            players_order=["a","b"],
            normal_size_limit=10
        )

base_turn = TurnRecord(
            bot_identifier="test",
            turn_number=1,
            origin_bullets=10,
            origin_fuel=10,
            origin_health=10,
            origin_position_x=10,
            origin_position_y=10,
            origin_shield_enabled=False,
            origin_victories=0,
            sent_payload="NOMATTER"
        )
base_player = _players_maker(1)[0]

PATCHED_ACTIONS = {
    "action_skip_turn": Mock(),
    "action_load_bullet": Mock(),
    "action_change_status_shield": Mock(),
    "action_tools": Mock(),
    "action_refuel": Mock(),
    "action_move": Mock(),
    "action_fire": Mock(),
    "dump_turn_to_botstatus": Mock(),
    "save_doc": Mock(),
}

@pytest.fixture
def reset_mocking():
    for _, mocked in PATCHED_ACTIONS.items():
        mocked.reset_mock()

def test_action_selection_with_no_response(reset_mocking):
    turn = base_turn.copy()
    with patch.multiple("app.game", **PATCHED_ACTIONS):
        process_response_of_player(
            game=base_game,
            turn=turn,
            player=base_player
        )
        PATCHED_ACTIONS["action_skip_turn"].assert_called_once()


def test_action_selection_with_response_not_valid(reset_mocking):
    turn = base_turn.copy()
    turn.received_response = "Unknow string"
    with patch.multiple("app.game", **PATCHED_ACTIONS):
        process_response_of_player(
            game=base_game,
            turn=turn,
            player=base_player
        )
        PATCHED_ACTIONS["action_skip_turn"].assert_called_once()

def test_action_selection_with_movement_response(reset_mocking):
    turn = base_turn.copy()
    turn.received_response = "M98989"
    with patch.multiple("app.game", **PATCHED_ACTIONS):
        process_response_of_player(
            game=base_game,
            turn=turn,
            player=base_player
        )
        PATCHED_ACTIONS["action_move"].assert_called_once()

def test_action_selection_with_fire_response(reset_mocking):
    turn = base_turn.copy()
    turn.received_response = "F12"
    with patch.multiple("app.game", **PATCHED_ACTIONS):
        process_response_of_player(
            game=base_game,
            turn=turn,
            player=base_player
        )
        PATCHED_ACTIONS["action_fire"].assert_called_once()


def test_action_selection_with_refuel_response(reset_mocking):
    turn = base_turn.copy()
    turn.received_response = "R"
    with patch.multiple("app.game", **PATCHED_ACTIONS):
        process_response_of_player(
            game=base_game,
            turn=turn,
            player=base_player
        )
        PATCHED_ACTIONS["action_refuel"].assert_called_once()

def test_action_selection_with_bullet_load_response(reset_mocking):
    turn = base_turn.copy()
    turn.received_response = "L"
    with patch.multiple("app.game", **PATCHED_ACTIONS):
        process_response_of_player(
            game=base_game,
            turn=turn,
            player=base_player
        )
        PATCHED_ACTIONS["action_load_bullet"].assert_called_once()

def test_action_selection_with_tools_response(reset_mocking):
    turn = base_turn.copy()
    turn.received_response = "T"
    with patch.multiple("app.game", **PATCHED_ACTIONS):
        process_response_of_player(
            game=base_game,
            turn=turn,
            player=base_player
        )
        PATCHED_ACTIONS["action_tools"].assert_called_once()

def test_action_selection_with_tools_response(reset_mocking):
    turn = base_turn.copy()
    turn.received_response = "S"
    with patch.multiple("app.game", **PATCHED_ACTIONS):
        process_response_of_player(
            game=base_game,
            turn=turn,
            player=base_player
        )
        PATCHED_ACTIONS["action_change_status_shield"].assert_called_once()
