import json
import itertools
from unittest.mock import patch, Mock
from app.game import play, get_all_players

def get_single_player(identifier):

    json_string = """
    {
        "_id": "-invalid-",
        "avatar_b64": null,
        "bot_identifier": "-invalid-",
        "built": false,
        "code": "fake_code",
        "creation_datetime": "2023-10-11T17:22:19.065Z",
        "dead": false,
        "email": "johndoe@example.com",
        "image_identifier": "sha256:b2bcc355f806e49fb91a52a26e8e3ecd77b57597a2f7e0a9c88e170786f367fe",
        "language": "python",
        "name": "John Doe"
    }
    """

    data_dict = json.loads(json_string)
    ident = f"bot{identifier}"
    data_dict["_id"] = ident
    data_dict["bot_identifier"] = ident
    data_dict["name"] = ident
    return data_dict

    
def patch_get_registered_players(cant):
    return [get_single_player(n) for n in range(cant) ]

LIST_PLAYERS = patch_get_registered_players(3)

def bot_assertions(bot):
    assert not bot.fuel < 0, "Fuel negative"
    assert not bot.health < 0, "Health negative"
    assert not bot.bullets < 0, "Bullets negative"
    assert bot.position_x > 0 and bot.position_y > 0, "Negative coords"

def patch_save_doc(*args, **kwargs):
    if str(args[0]) == 'Databases.PLAYERS':
        for bot in LIST_PLAYERS:
            if bot['bot_identifier'] == args[1].bot_identifier:
                bot.update(args[1].export())
                bot_assertions(args[1])
                break
        coords = {(p.get("position_x", p["bot_identifier"]), p.get("position_y", p["bot_identifier"])) for p in LIST_PLAYERS}
        assert len(coords) == len(LIST_PLAYERS), "There are many player with the same coord"
        


@patch("app.game.get_registered_players", return_value=LIST_PLAYERS)
@patch("app.game.load_ongoing_game", return_value=None)
@patch("app.game.save_doc")
def test_play_1(patched_save_doc, patched_load, patched_all_players):
    side_effect = itertools.cycle(get_all_players())
    patcher = patch("app.game._choice_next_player", side_effect=side_effect)
    patched_save_doc.side_effect = patch_save_doc
    patcher.start()
    play()
    patcher.stop()
    assert False