import pytest
from pytest import MonkeyPatch
from unittest.mock import patch, Mock

from app.models import Player
from app.game import randomize_positions

def patch_settings(patch_instance, overwrite: dict = None):
    over = overwrite if overwrite else {}
    var_default_value = {
        "FUEL_CONSUMED_BY_TURN": 1,
        "FUEL_CONSUMED_BY_TURN_WITH_SHIELD": 2,
        "DEFAULT_VISIBILY_DISTANCE": 3,
        "DAMAGE_BY_HIT": 10,
        "SHIELD_PROTECTION_PERCENTAGE": 50,
        "DEFAULT_WIDTH": 20,
        "DEFAULT_HEIGHT": 20,
        "DAMAGE_BY_BULLET": 20
    }
    for name, v in var_default_value.items():
        if name in over.keys():
            value = over[name]
        else:
            value = v
        patch_instance.setattr(f"app.game.{name}", value)


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
def test_normal_board(patched_save_doc, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch)
    players = _players_maker(5)
    randomize_positions(players=players)
    patched_save_doc.assert_called()
    for call in patched_save_doc.mock_calls:
        assert call[1][1].position_x < 20  # DEFAULT_WIDTH
        assert call[1][1].position_y < 20  # DEFAULT_HEIGHT



@patch("app.game.save_doc")
def test_too_small_board(patched_save_doc, monkeypatch: MonkeyPatch):
    patch_settings(monkeypatch, {"DEFAULT_WIDTH": 5, "DEFAULT_HEIGHT": 5})
    players = _players_maker(30)
    with pytest.raises(Exception, match="Board too small for 30 players"):
        randomize_positions(players=players)
    patched_save_doc.assert_not_called()
