from random import shuffle, choice
from fastapi.logger import logger
from app.rpc.grpc_main import call_to_bot
# from app.models import PlayerLoader
from app.settings import (
    DEFAULT_STOP_LIMIT,
    NORMAL_SIZE_LIMIT,
    DEFAULT_VISIBILY_DISTANCE,
    DEFAULT_HEIGHT,
    DEFAULT_WIDTH,
    DECREMENT_AFTER_LIMIT,
    FUEL_CONSUMED_BY_TURN,
    FUEL_CONSUMED_BY_TURN_WITH_SHIELD,
    FOE_SYMBOL,
    DAMAGE_BY_BULLET,
    DAMAGE_BY_HIT,
    SHIELD_PROTECTION_PERCENTAGE,
    WALL_SYMBOL,
    PLAYER_POSITION_IDENTIFICACION,
    DEFAULT_EMPTY_PLACE_SYMBOL,
    REFUEL_BY_TURN,
    REPAIR_BY_TURN,
    RELOAD_BY_TURN,
    MAX_HEALTH,
    MAX_BULLET,
    MAX_FUEL,
)

from .db import (
    load_doc,
    save_doc,
    Databases,
    get_players_in_area,
    get_running_games,
    load_events_for_game,
    load_turns_for_game,
    get_registered_players,
    get_bots
)

from .models import (
    Player,
    GameSession,
    GameEvent,
    TurnRecord,
    ActionOfBot,
    GameEventType
)

assert DEFAULT_WIDTH == DEFAULT_HEIGHT, "For now only with square board. Tag: B001"
global current_board_width, current_board_height
current_board_width, current_board_height = DEFAULT_WIDTH, DEFAULT_HEIGHT

def start_new_game(*,
                   players:list[Player],
                   width: int,
                   height: int) -> tuple[GameSession, bool]:
    current_game = load_ongoing_game()
    if current_game:
        return current_game, True
    if not players:
        logger.debug("Receive null parameter")
        raise ValueError("Need players for play")
    players_id = {pyr.bot_identifier for pyr in players}
    list_players = list(players_id)
    shuffle(list_players)
    logger.info(f"Starting game with {len(list_players)} players")
    session = GameSession(
        initial_players=players_id,
        current_players=players_id,
        players_order=list_players,
        normal_size_limit=NORMAL_SIZE_LIMIT,
        board_size_x=width,
        board_size_y=height
    )
    save_doc(Databases.GAMES, session)
    return session, False


def load_ongoing_game() -> None | GameSession:
    """Return the ongoing game if exists"""
    ongoing = get_running_games()
    if ongoing:
        if len(ongoing) > 1:
            logger.warning("There are many ongoing games")
        return GameSession(**ongoing[0])
    return None


def find_existent_bot(bot_id: str, email: str) -> tuple[bool, bool]:
    bots = get_bots(bot_id)
    if not len(bots):
        return False, False

    return True, bots[0].email == email


def register_new_player(registrant, image_id: str):
    registrant.image_identifier = image_id
    save_doc(Databases.PLAYERS, registrant)


def _choice_next_player(session: GameSession) -> Player:
    if session.last_bot_played is None:
        index = 0
        register_event(session, GameEventType.START_GAME)
    else:
        index = session.players_order.index(session.last_bot_played) + 1
        index = 0 if index == len(session.players_order) else index
        if index == 0:
            register_event(session, GameEventType.END_ROUND)
    
    chosen = session.players_order[index]

    return load_player(chosen)

def _get_previous_in_order(session: GameSession, reference_bot_id: str) -> Player:
    index = session.players_order.index(reference_bot_id) - 1
    if index == -1:
        index = len(session.players_order) - 1
    return session.players_order[index]


def load_player(bot_id: str) -> Player:
    doc = load_doc(Databases.PLAYERS, document_id=bot_id)
    return Player(**doc)


def get_players_in_environment(player: Player) -> list[Player]:
    def evaluate_element_of_window(component: int, difference: int) -> int:
        position = component + difference
        if position > current_board_height:  # TAG: B001
            position = current_board_width
        if position < 0:
            position = 0
        return position

    current_x = player.position_x
    current_y = player.position_y
    window = (
        evaluate_element_of_window(current_x, -DEFAULT_VISIBILY_DISTANCE),
        evaluate_element_of_window(current_y, -DEFAULT_VISIBILY_DISTANCE),
        evaluate_element_of_window(current_x, +DEFAULT_VISIBILY_DISTANCE),
        evaluate_element_of_window(current_y, +DEFAULT_VISIBILY_DISTANCE)
    )
    players = [Player(**p) for p in get_players_in_area(window)]
    return players


def get_player_environment(player: Player):
    player_in_environment = get_players_in_environment(player)
    x, y = player.position_x, player.position_y
    right_wall = current_board_width - x
    left_wall = -x - 1
    up_wall = -y - 1
    down_wall = current_board_width - y
    enemy_by_relative_coord = {(p.position_x - x, p.position_y - y): p for p in player_in_environment}
    environment = []
    for row in range(-DEFAULT_VISIBILY_DISTANCE, DEFAULT_VISIBILY_DISTANCE +1):
        row_data = []
        for col in range(-DEFAULT_VISIBILY_DISTANCE, DEFAULT_VISIBILY_DISTANCE +1):
            symbol = DEFAULT_EMPTY_PLACE_SYMBOL
            if any([
                row <= up_wall,
                row >= down_wall,
                col <= left_wall,
                col >= right_wall
            ]):
                symbol = WALL_SYMBOL
            if (col, row) in enemy_by_relative_coord.keys():
                symbol = FOE_SYMBOL
            if row == 0 and col == 0:
                symbol = PLAYER_POSITION_IDENTIFICACION
            row_data.append(symbol)
        environment.append(row_data)
    return environment


def stringfy_parameter(player: Player, environment: list[list[str]]):
    flat_environment = "".join(["".join(elem) for elem in environment])
    shield = "T" if player.shield_mounted else "F"
    flat_environment += f"{player.fuel:02}{player.bullets:02}{player.health:02}{shield}"
    return flat_environment


def make_call_to_bot(player: Player, parameter: str) -> str:
    return call_to_bot(player.bot_identifier, parameter)


def play_next_turn(game: GameSession) -> TurnRecord:
    player = _choice_next_player(game)
    
    environment = get_player_environment(player)
    turn_parameter = stringfy_parameter(player, environment)
    turn = TurnRecord(
        bot_identifier=player.bot_identifier,
        session_identifier=game.session_identifier,
        turn_number=game.current_turn,
        origin_position_x=player.position_x,
        origin_position_y=player.position_y,
        origin_bullets=player.bullets,
        origin_fuel=player.fuel,
        origin_health=player.health,
        origin_victories=player.victories,
        sent_payload=turn_parameter
    )
    logger.debug(f"Calling bot {player.bot_identifier} with {turn_parameter}")
    response = make_call_to_bot(player, turn_parameter)
    turn.received_response = response
    return turn


def get_all_players() -> list[Player]:
    players_list_of_dict = get_registered_players(True)
    return [Player(**item) for item in players_list_of_dict]


def _board_coords_maker(limit_x, limit_y) -> list[tuple]:
    board = []
    for row in range(limit_y or current_board_height):
        for col in range(limit_x or current_board_width):
            board.append(
                (col, row)
            )
    return board


def randomize_positions(players: list[Player], limit_x: int | None = None, limit_y: int | None = None):
    board_coords = _board_coords_maker(limit_x, limit_y)
    if len(players) > len(board_coords):
        raise Exception(f"Board too small for {len(players)} players")
    shuffle(board_coords)
    for player in players:
        coord = board_coords.pop()
        player.position_x, player.position_y = coord
        save_doc(Databases.PLAYERS, player)


def reduce_board_size(*, game: GameSession, step_down:int) -> GameSession:
    vertical_window = (
        game.board_size_x - step_down,
        0,
        game.board_size_x,
        game.board_size_y
    )
    horizontal_window = (
        0,
        game.board_size_y - step_down,
        game.board_size_x - step_down - 1,
        game.board_size_y
    )

    if not len(game.current_players) > (game.board_size_x * game.board_size_y):
        game.board_size_x -= step_down
        game.board_size_y -= step_down
        register_event(game=game, event_type=GameEventType.BOARD, info=f"Resize to {game.board_size_x},{game.board_size_y}") 

    player_in_vertical_area = get_players_in_area(vertical_window)
    player_in_horizontal_area = get_players_in_area(horizontal_window)
    player_in_vertical_area.extend(player_in_horizontal_area)
    players = [Player(**p) for p in player_in_vertical_area]

    current_board_width, current_board_height = game.board_size_x, game.board_size_y
    randomize_positions(players, limit_x=game.board_size_x, limit_y=game.board_size_y)


def action_skip_turn(game: GameSession, turn: TurnRecord) -> TurnRecord:
    turn.action = ActionOfBot.SKIPPED.value
    turn.final_bullets = turn.origin_bullets if not turn.final_bullets else turn.final_bullets
    turn.final_health = turn.origin_health if not turn.final_health else turn.final_health
    turn.final_position_x = turn.origin_position_x if not turn.final_position_x else turn.final_position_x
    turn.final_position_y = turn.origin_position_y if not turn.final_position_y else turn.final_position_y
    turn.final_victories = turn.origin_victories if not turn.final_victories else turn.final_victories
    turn.final_fuel = turn.origin_fuel - FUEL_CONSUMED_BY_TURN if not turn.final_fuel else turn.final_fuel
    return turn


def action_fire(game: GameSession, turn: TurnRecord) -> TurnRecord:

    turn.action = ActionOfBot.FIRE.value
    _copy_turn_status_origin_to_final(turn)

    cmd = turn.received_response[:3] if turn.received_response else "XXX"
    target_x, target_y = cmd[1], cmd[2]
    turn.final_bullets = turn.origin_bullets - 1  # If wrong response, lose a bullet
    turn.final_fuel = turn.origin_fuel - consumed_fuel(turn, 0)
    try:
        assert target_x.isnumeric, "Invalid coord"
        assert target_y.isnumeric, "Invalid coord"
        target_x = int(target_x)
        target_y = int(target_y)
        assert target_x <= DEFAULT_VISIBILY_DISTANCE * 2 + 1, "Invalid coord"
        assert target_y <= DEFAULT_VISIBILY_DISTANCE * 2 + 1, "Invalid coord"
        assert turn.origin_bullets > 0, "No bullets"
        assert turn.origin_fuel > 0, "No fuel"
    except AssertionError as e:
        turn.notes = e.args[0]
        turn.wrong_response = True
        if turn.final_bullets < 0:
            turn.final_bullets = 0
        return action_skip_turn(game, turn)

    environment = decode_environment(turn.sent_payload)
    enemy_positions = [k for k, v in environment.get("by_coord", {}).items() if v == FOE_SYMBOL]
    
    abs_position = make_absolute_coord(
        original_value=(turn.origin_position_x, turn.origin_position_y),
        relative_position=(target_x, target_y)
    )
    turn.target_abs_coordinates = str(abs_position)
    if (target_x, target_y) in enemy_positions:
        turn = enemy_reached(game=game, turn=turn, position=abs_position)
        turn.target_reached = True
    return turn


def enemy_reached(*, game: GameSession, turn: TurnRecord, position: tuple) -> TurnRecord:
    x, y = position
    damage_on_hit = DAMAGE_BY_BULLET
    try:
        hit_player = Player(**get_players_in_area(window=(x, y, x, y))[0])
    except IndexError:
        print("// Error //")
    if hit_player.shield_mounted:
        damage_on_hit = int(damage_on_hit * SHIELD_PROTECTION_PERCENTAGE / 100)
    hit_player.health -= damage_on_hit
    if dead_player(game=game, player=hit_player):
        turn.final_victories = turn.origin_victories + 1
        hit_player.health = 0
    
    save_doc(Databases.PLAYERS, hit_player)
    return turn


def decode_environment(payload: str) -> dict:
    def _get_element_position(substr: str, identification: str) -> list:
        row, col, last_found = 0, 0, 0
        response = []
        while True:
            try:
                enemy_position = substr.index(identification, last_found)
            except ValueError:
                break
            last_found = enemy_position + 1
            row = int(enemy_position / scope)
            col = enemy_position - row * scope
            response.append((col, row))
        return response

    scope = (DEFAULT_VISIBILY_DISTANCE * 2) + 1 
    substr_payload = payload[:scope*scope]
    enemies = _get_element_position(substr_payload, FOE_SYMBOL)
    walls = _get_element_position(substr_payload, WALL_SYMBOL)
    by_coord = {coord: FOE_SYMBOL for coord in enemies}
    by_coord.update({coord: WALL_SYMBOL for coord in walls})
    
    response = {
        "enemies": enemies,
        "walls": walls, 
        "by_coord": by_coord
    }

    return response


def register_event(game: GameSession, event_type: GameEventType, info: str | None = None):
    event = GameEvent(
        session_identifier=game.session_identifier,
        event_type=event_type,
        aditional_info=info
    )
    save_doc(Databases.BOARD_EVENTS, event)


def remove_player_from_game(game: GameSession, bot_identifier: str, playing_bot: bool = False) -> GameSession:
    previous_bot = _get_previous_in_order(game, bot_identifier)
    game.current_players.remove(bot_identifier)
    game.players_order.remove(bot_identifier)
    save_doc(Databases.GAMES, game)
    if playing_bot:
        game.last_bot_played = previous_bot  # set reference to continue the right bot's turn
    return game


def dead_player(game: GameSession, player: Player) -> bool:
    dead = player.health <= 0
    if dead:
        player.health = 0
        player.dead = True
        register_event(
            game=game,
            event_type=GameEventType.SOME_DIED,
            info=player.bot_identifier
        )
        game = remove_player_from_game(
            game=game,
            bot_identifier=player.bot_identifier,
            playing_bot=game.last_bot_played == player.bot_identifier
        )
    return dead


def fight_by_collision(game: GameSession, turn: TurnRecord, target_player: Player) -> TurnRecord:
    damage_on_source_player = DAMAGE_BY_HIT
    damage_on_target_player = DAMAGE_BY_HIT
    if turn.origin_shield_enabled:
        damage_on_source_player = int(damage_on_source_player * SHIELD_PROTECTION_PERCENTAGE / 100)
    if target_player.shield_mounted:
        damage_on_target_player = int(damage_on_target_player * SHIELD_PROTECTION_PERCENTAGE / 100)

    turn.final_health = turn.origin_health - damage_on_source_player
    target_player.health -= damage_on_target_player
    turn.collision = True
    turn.collision_to = target_player.bot_identifier
    dead_target = dead_player(game=game, player=target_player)
    save_doc(Databases.PLAYERS, target_player)
    if dead_target:
        turn.final_victories = turn.origin_victories + 1
    return turn


def wall_collision_damage(game: GameSession, turn: TurnRecord) -> TurnRecord:
    damage = DAMAGE_BY_HIT
    if turn.origin_shield_enabled:
        damage = int(damage * SHIELD_PROTECTION_PERCENTAGE / 100)
    turn.final_health = turn.origin_health - damage
    turn.collision = True
    return turn


def _find_a_new_position(coord: tuple, occupied_positions: set) -> tuple:
    new_x, new_y = coord
    variation_x = 1 if new_x < DEFAULT_VISIBILY_DISTANCE else -1
    variation_y = 1 if new_y < DEFAULT_VISIBILY_DISTANCE else -1
    if new_x == DEFAULT_VISIBILY_DISTANCE:
        variation_x = 0
    if new_y == DEFAULT_VISIBILY_DISTANCE:
        variation_y = 0
                
    collided = True
    whatchdog = 0
    whatchdog_limit = (DEFAULT_VISIBILY_DISTANCE * 2 + 1) ** 2
    while collided:
        whatchdog += 1
        if whatchdog > whatchdog_limit:
            return (3, 3)
        if DEFAULT_VISIBILY_DISTANCE - abs(new_x) > 0:
            new_x += variation_x
            if (new_x, new_y) in occupied_positions:
                continue
            collided = False
            continue
        if DEFAULT_VISIBILY_DISTANCE - abs(new_y) > 0:
            new_y += variation_y
            if (new_x, new_y) in occupied_positions:
                continue
            collided = False
            continue
        if collided:
            new_x, new_y = 0, 0
    return (new_x, new_y)


def manage_enemy_collision(*,
                           game: GameSession,
                           turn: TurnRecord,
                           coord: tuple) -> TurnRecord:
    _turn = turn
    x, y = coord
    collided_player = Player(**get_players_in_area(window=(x, y, x, y))[0])
    _turn = fight_by_collision(
        game=game,
        turn=turn,
        target_player=collided_player
    )
    register_event(
        game=game,
        event_type=GameEventType.COLLISION,
        info=f"{turn.bot_identifier},{collided_player.bot_identifier}"
    )

    return _turn


def dump_turn_to_botstatus(*, game: GameSession,
                              player: Player,
                              turn: TurnRecord) -> None:
    player.bullets = turn.final_bullets or 0 
    player.health = turn.final_health or 0
    player.fuel = turn.final_fuel if turn.final_fuel > 0 else 0
    player.shield_mounted = turn.final_shield_enabled or False
    player.position_x = turn.final_position_x or 0
    player.position_y = turn.final_position_y or 0
    player.victories = turn.final_victories or 0
    player.dead = dead_player(game, player)
    save_doc(Databases.PLAYERS, player)


def manage_wall_collision(*,
                          game: GameSession,
                          turn: TurnRecord,
                          coord: tuple) -> TurnRecord:
    _turn = wall_collision_damage(game, turn)
    return _turn


def make_absolute_coord(*, original_value: tuple, relative_position: tuple) -> tuple:
    _centered_x = relative_position[0] - DEFAULT_VISIBILY_DISTANCE
    _centered_y = relative_position[1] - DEFAULT_VISIBILY_DISTANCE
    _new_x = original_value[0] + _centered_x
    _new_y = original_value[1] + _centered_y
    return (
        _new_x if _new_x > 0 else 0,
        _new_y if _new_y > 0 else 0
    )


def _copy_turn_status_origin_to_final(turn: TurnRecord) -> None:
    turn.final_bullets = turn.origin_bullets
    turn.final_fuel = turn.origin_fuel
    turn.final_health = turn.origin_health
    turn.final_position_x = turn.origin_position_x
    turn.final_position_y = turn.origin_position_y
    turn.final_shield_enabled = turn.origin_shield_enabled
    turn.final_victories = turn.origin_victories


def consumed_fuel(turn: TurnRecord, cells_moved: int):
    fuel_consumption = FUEL_CONSUMED_BY_TURN_WITH_SHIELD if \
        turn.origin_shield_enabled else FUEL_CONSUMED_BY_TURN
    if cells_moved > 2:
        consumed_fuel = (fuel_consumption + 1) ** (cells_moved - 1)
    else:
        consumed_fuel = (cells_moved or 1) * fuel_consumption
    return consumed_fuel


def action_move(game: GameSession, turn: TurnRecord) -> TurnRecord:

    def calculate_moved_cells(x, y):
        moved_x = abs(x - DEFAULT_VISIBILY_DISTANCE)
        moved_y = abs(y - DEFAULT_VISIBILY_DISTANCE)
        return moved_x + moved_y
    
    turn.action = ActionOfBot.MOVE.value
    _copy_turn_status_origin_to_final(turn)
    turn.final_fuel = None  # in case wrong response, so skip decrement it

    cmd = turn.received_response[:3] if turn.received_response else "XXX"
    x, y = cmd[1], cmd[2]

    try:
        assert x.isnumeric, "Invalid coord"
        assert y.isnumeric, "Invalid coord"
        x = int(x)
        y = int(y)
        assert x <= DEFAULT_VISIBILY_DISTANCE * 2 + 1, "Invalid coord"
        assert y <= DEFAULT_VISIBILY_DISTANCE * 2 + 1, "Invalid coord"
        assert turn.origin_fuel > 0, "No fuel"
    except AssertionError as e:
        turn.notes = e.args[0]
        turn.wrong_response = True
        return action_skip_turn(game, turn)


    cells_moved = calculate_moved_cells(x,y)

    used_fuel = consumed_fuel(turn, cells_moved)
    if turn.origin_fuel < used_fuel:
        turn.wrong_response = True
        return action_skip_turn(game=game, turn=turn)
    
    turn.final_fuel = turn.origin_fuel - used_fuel
    environment = decode_environment(turn.sent_payload)
    occupied_positions = set(environment.get("by_coord", {}).keys())
    
    collided_with = environment.get("by_coord", {}).get((x, y))

    while collided_with:
        abs_x, abs_y = make_absolute_coord(
            original_value=(turn.origin_position_x, turn.origin_position_y),
            relative_position=(x, y)
        )  
        if collided_with == FOE_SYMBOL:
            turn = manage_enemy_collision(
                game=game,
                turn=turn,
                coord=(abs_x, abs_y)
            )
        if collided_with == WALL_SYMBOL:
            turn = manage_wall_collision(
                game=game,
                turn=turn,
                coord=(abs_x, abs_y)
            )
        x, y = _find_a_new_position((x, y), occupied_positions)
        collided_with = environment.get("by_coords", {}).get((x, y))

    abs_x, abs_y = make_absolute_coord(
        original_value=(turn.origin_position_x, turn.origin_position_y),
        relative_position=(x, y)
    )
    turn.final_position_x, turn.final_position_y = abs_x, abs_y 
    return turn


def action_refuel(game: GameSession, turn: TurnRecord) -> TurnRecord:
    _copy_turn_status_origin_to_final(turn)
    turn.action = ActionOfBot.REFUEL.value
    used_fuel = consumed_fuel(turn, 0)
    current_fuel = turn.origin_fuel + REFUEL_BY_TURN
    current_fuel = current_fuel if current_fuel <= MAX_FUEL else MAX_FUEL
    turn.final_fuel = current_fuel - used_fuel


    return turn


def action_tools(game: GameSession, turn: TurnRecord) -> TurnRecord:
    _copy_turn_status_origin_to_final(turn)
    try:
        assert turn.origin_fuel > 0, "No fuel"
    except AssertionError as e:
        turn.notes = e.args[0]
        return action_skip_turn(game, turn)

    turn.action = ActionOfBot.TOOLS.value
    current_health = turn.origin_health + REPAIR_BY_TURN
    turn.final_health = current_health if current_health <= MAX_HEALTH else MAX_HEALTH
    used_fuel = consumed_fuel(turn, 0)
    turn.final_fuel = turn.origin_fuel - used_fuel
    return turn


def action_change_status_shield(game: GameSession, turn: TurnRecord) -> TurnRecord:
    _copy_turn_status_origin_to_final(turn)
    turn.action = ActionOfBot.SHIELD.value
    turn.final_shield_enabled = not turn.origin_shield_enabled
    used_fuel = consumed_fuel(turn, 0)
    turn.final_fuel = turn.origin_fuel - used_fuel
    return turn


def action_load_bullet(game: GameSession, turn: TurnRecord) -> TurnRecord:
    _copy_turn_status_origin_to_final(turn)
    turn.action = ActionOfBot.LOAD.value
    turn.final_bullets = turn.origin_bullets + RELOAD_BY_TURN
    turn.final_bullets = turn.final_bullets if turn.final_bullets <= MAX_BULLET else MAX_BULLET
    used_fuel = consumed_fuel(turn, 0)    
    turn.final_fuel = turn.origin_fuel - used_fuel
    return turn


def _save_turn_results(*, turn: TurnRecord) -> None:
    save_doc(Databases.TURNS, turn)


def process_response_of_player(*, 
                               game: GameSession,
                               player: Player,
                               turn: TurnRecord) -> TurnRecord:
    response = turn.received_response or "/"
    response = response.upper()
    match response[0]:
        case ActionOfBot.FIRE.value:
            action = action_fire
        case ActionOfBot.MOVE.value:
            action = action_move
        case ActionOfBot.REFUEL.value:
            action = action_refuel
        case ActionOfBot.TOOLS.value:
            action = action_tools
        case ActionOfBot.SHIELD.value:
            action = action_change_status_shield
        case ActionOfBot.LOAD.value:
            action = action_load_bullet
        case other:
            action = action_skip_turn
    executed_turn = action(game=game, turn=turn)
    dump_turn_to_botstatus(game=game, player=player, turn=turn)
    return executed_turn


def save_game_status(game: GameSession):
    save_doc(Databases.GAMES, game)


def execute_loop(game: GameSession) -> str:
    game.current_turn = 0
    while not game.winner:

        player_turn = play_next_turn(game)
        player = load_player(player_turn.bot_identifier)
        game.last_bot_played = player.bot_identifier
        played_turn = process_response_of_player(
            game=game,
            player=player,
            turn=player_turn
        )
        _save_turn_results(turn=played_turn)
        if len(game.current_players) == 1:
            game.winner = list(game.current_players)[0]
            break

        game.current_turn = game.current_turn + 1      

        if game.current_turn > DEFAULT_STOP_LIMIT:
            raise Exception("Limit of turns reached")
            
    
        if (game.current_turn > NORMAL_SIZE_LIMIT) and (game.board_size_x > 6):
            reduce_board_size(game=game, step_down=DECREMENT_AFTER_LIMIT)
        save_game_status(game)
    return game.winner
            

def get_events(game: GameSession) -> list[GameEvent]:
    return load_events_for_game(game._id)


def get_turns(game: GameSession) -> list[TurnRecord]:
    return load_turns_for_game(game._id)


def play() -> dict:
    all_players = get_all_players()
    if not all_players or len(all_players) < 2:
        raise ValueError("There is no players registered for this game")

    game, ongoing = start_new_game(players = all_players, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)
    if not ongoing:
        randomize_positions(all_players)
    winner = execute_loop(game)
    events = get_events(game)
    turns = get_turns(game)
    names = { item.bot_identifier: item.name for item in all_players}
    return {
        "players": all_players,
        "winner": winner,
        "events": events,
        "turns": turns,
        "names": names
    }
