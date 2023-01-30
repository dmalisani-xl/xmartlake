from unittest.mock import patch

from app.models import Player, GameSession
from app.game import start_new_game


def _players_maker(quantity: int) -> list[Player]:
    list_of_players = []
    for x in range(quantity-1):
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
    game = start_new_game(players=players, width=100, height=200)
    assert type(game) == GameSession
    assert set(game.current_players) == set(game.initial_players)
    assert len(game.initial_players) == len(game.players_order)
    patched_save_doc.assert_called_once()
