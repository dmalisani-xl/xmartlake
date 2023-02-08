from random import shuffle

from app.settings import (
    NORMAL_SIZE_LIMIT,
    DEFAULT_VISIBILY_DISTANCE,
    DEFAULT_HEIGHT,
    DEFAULT_WIDTH,
    FUEL_CONSUMED_BY_TURN,
    FUEL_CONSUMED_BY_TURN_WITH_SHIELD,
    FOE_IDENTIFICATION,
    DAMAGE_BY_BULLET,
    DAMAGE_BY_HIT,
    SHIELD_PROTECTION_PERCENTAGE,
    WALL_IDENTIFICATION
)

from .db import save_doc, Databases, get_players_in_area
from .models import (
    Player,
    GameSession,
    GameEvent,
    TurnRecord,
    ActionOfBot,
    GameEventType
)

assert DEFAULT_WIDTH == DEFAULT_HEIGHT, "For now only with square board. Tag: B001"


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
        normal_size_limit=NORMAL_SIZE_LIMIT,
        board_size_x=width,
        board_size_y=height
    )
    save_doc(Databases.GAMES, session)
    return session


def load_ongoing_game() -> None | GameSession:
    """Return the ongoing game if exists"""


def _choice_next_player(session: GameSession) -> Player:
    ...


def _load_player(bot_id: str) -> Player:
    ...


def get_players_in_environment(player: Player) -> list[Player]:
    def evaluate_element_of_window(component: int, difference: int) -> int:
        position = component + difference
        if position > DEFAULT_HEIGHT:  # TAG: B001
            position = DEFAULT_WIDTH
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
    players = [Player(**p) for p in get_players_in_area(**window)]
    return players


def stringfy_parameter(player: Player, environment: list[list[str]]):
    ...


def call_to_bot(player: Player, parameter: str) -> str:
    ...


def play_next_turn(game: GameSession) -> TurnRecord:
    player_id = _choice_next_player(game)
    player = _load_player(player_id)
    environment = get_players_in_environment(player)
    turn_parameter = stringfy_parameter(player, environment)
    turn = TurnRecord(
        bot_identifier=player_id,
        turn_number=game.current_turn,
        origin_position_x=player.position_x,
        origin_position_y=player.position_y,
        origin_bullets=player.bullets,
        origin_fuel=player.fuel,
        origin_health=player.health,
        origin_victories=player.victories,
        sent_payload=turn_parameter
    )
    response = call_to_bot(player, turn_parameter)
    turn.received_response = response
    return turn


def _get_all_players() -> list[Player]:
    ...


def randomize_positions(players: list[Player]):
    # Need detect overlaping
    # Save positions to db
    ...

def reduce_board_size(game: GameSession, step_down:int) -> GameSession:
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
    player_in_vertical_area = get_players_in_area(vertical_window)
    player_in_horizontal_area = get_players_in_area(horizontal_window)
    player_in_vertical_area.extend(player_in_horizontal_area)
    players = [Player(**p) for p in player_in_vertical_area]
    randomize_positions(players)

def action_skip_turn(game: GameSession, turn: TurnRecord) -> TurnRecord:
    turn.action = ActionOfBot.SKIPPED.value
    turn.final_bullets = turn.origin_bullets
    turn.final_health = turn.origin_health
    turn.final_position_x = turn.origin_position_x
    turn.final_position_y = turn.origin_position_y
    turn.final_victories = turn.origin_victories
    turn.final_fuel = turn.origin_fuel - FUEL_CONSUMED_BY_TURN
    return turn

def action_fire(game: GameSession, turn: TurnRecord) -> TurnRecord:
    raise NotImplementedError


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
            response.append((row, col))
        return response

    scope = (DEFAULT_VISIBILY_DISTANCE * 2) + 1 
    substr_payload = payload[:scope*scope]
    enemies = _get_element_position(substr_payload, FOE_IDENTIFICATION)
    walls = _get_element_position(substr_payload, WALL_IDENTIFICATION)
    by_coord = {coord: FOE_IDENTIFICATION for coord in enemies}
    by_coord.update({coord: WALL_IDENTIFICATION for coord in walls})
    
    response = {
        "enemies": enemies,
        "walls": walls, 
        "by_coord": by_coord
    }


    return response
 

def encode_environment( environment: list[list[str]]) -> str:
    raise NotImplementedError


def register_event(game: GameSession, event_type: GameEventType, info: str | None = None):
    event = GameEvent(
        session_identifier=game.session_identifier,
        event_type=event_type,
        aditional_info=info
    )
    save_doc(Databases.BOARD_EVENTS, event)

def remove_player_from_game(game: GameSession, bot_identifier: str) -> GameSession:
    game.current_players.remove(bot_identifier)
    save_doc(Databases.GAMES, game)
    return game

def dead_player(game: GameSession, player: Player) -> bool:
    dead = player.health <= 0
    if dead:
        player.health = 0
        register_event(
            game=game,
            event_type=GameEventType.SOME_DIED,
            info=player.bot_identifier
        )
        game = remove_player_from_game(
            game=game,
            bot_identifier=player.bot_identifier
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
    turn.hit = True
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
    turn.hit = True
    return turn


def _find_a_new_position(coord: tuple, occupied_positions: set) -> tuple:
    new_x, new_y = coord
    variation_x = 1 if new_x < DEFAULT_VISIBILY_DISTANCE else -1
    variation_y = 1 if new_y < DEFAULT_VISIBILY_DISTANCE else -1
    collided = True
    while collided:
        if new_x > 0:
            new_x += variation_x
            if (new_x, new_y) in occupied_positions:
                continue
            collided = False
            continue
        if new_y > 0:
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
    hit_player = Player(**get_players_in_area(window=(x, y, x, y)))
    _turn = fight_by_collision(
        game=game,
        turn=turn,
        target_player=hit_player
    )
    register_event(
        game=game,
        event_type=GameEventType.HIT,
        info=f"{turn.bot_identifier},{hit_player.bot_identifier}"
    )

    return _turn


def manage_wall_collision(*,
                          game: GameSession,
                          turn: TurnRecord,
                          coord: tuple) -> TurnRecord:
    _turn = wall_collision_damage(game, turn)
    return _turn
        
def _make_absolute_coord(*, original_value: tuple, relative_position: tuple) -> tuple:
    _centered_x = relative_position[0] - DEFAULT_VISIBILY_DISTANCE
    _centered_y = relative_position[1] - DEFAULT_VISIBILY_DISTANCE
    return (
        original_value[0] + _centered_x,
        original_value[0] + _centered_y,
    )

def _copy_turn_status_origin_to_final(turn: TurnRecord) -> None:
    turn.final_bullets = turn.origin_bullets
    turn.final_fuel = turn.origin_fuel
    turn.final_health = turn.origin_health
    turn.final_position_x = turn.origin_position_x
    turn.final_position_y = turn.origin_position_y
    turn.final_shield_enabled = turn.origin_shield_enabled
    turn.final_victories = turn.origin_victories

def action_move(game: GameSession, turn: TurnRecord) -> TurnRecord:

    def calculate_moved_cells(x, y):
        moved_x = abs(x - DEFAULT_VISIBILY_DISTANCE)
        moved_y = abs(y - DEFAULT_VISIBILY_DISTANCE)
        return moved_x + moved_y
    
    def consumed_fueld(cells_moved: int):
        fuel_consumption = FUEL_CONSUMED_BY_TURN_WITH_SHIELD if \
            turn.origin_shield_enabled else FUEL_CONSUMED_BY_TURN
        if cells_moved > 2:
            consumed_fuel = (fuel_consumption + 1) ** (cells_moved - 1)
        else:
            consumed_fuel = (cells_moved or 1) * fuel_consumption
        return consumed_fuel

    turn.action = ActionOfBot.MOVE.value
    _copy_turn_status_origin_to_final(turn)

    cmd = turn.received_response[:3]
    x, y = cmd[1], cmd[2]

    try:
        assert x.isnumeric
        assert y.isnumeric
        x = int(x)
        y = int(y)
        assert x <= DEFAULT_VISIBILY_DISTANCE * 2 + 1
        assert y <= DEFAULT_VISIBILY_DISTANCE * 2 + 1
    except AssertionError:
        turn.wrong_response = True
        return action_skip_turn(game, turn)


    cells_moved = calculate_moved_cells(x,y)

    used_fuel = consumed_fueld(cells_moved)
    if turn.origin_fuel < used_fuel:
        turn.wrong_response = True
        return action_skip_turn(turn)
    
    turn.final_fuel = turn.origin_fuel - used_fuel
    environment = decode_environment(turn.sent_payload)
    occupied_positions = set(environment.get("by_coord").keys())
    
    collided_with = environment.get("by_coord", {}).get((x, y))

    while collided_with:
        abs_x, abs_y = _make_absolute_coord(
            original_value=(turn.origin_position_x, turn.origin_position_y),
            relative_position=(x, y)
        )  
        if collided_with == FOE_IDENTIFICATION:
            turn = manage_enemy_collision(
                game=game,
                turn=turn,
                coord=(abs_x, abs_y)
            )
        if collided_with == WALL_IDENTIFICATION:
            turn = manage_wall_collision(
                game=game,
                turn=turn,
                coord=(abs_x, abs_y)
            )
        x, y = _find_a_new_position((x, y), occupied_positions)
        collided_with = environment.get("by_coords", {}).get((x, y))

    abs_x, abs_y = _make_absolute_coord(
        original_value=(turn.origin_position_x, turn.origin_position_y),
        relative_position=(x, y)
    )
    turn.final_position_x, turn.final_position_y = abs_x, abs_y 
    return turn

def action_refuel(game: GameSession, turn: TurnRecord) -> TurnRecord:
    raise NotImplementedError

def action_tools(game: GameSession, turn: TurnRecord) -> TurnRecord:
    raise NotImplementedError

def action_change_status_shield(game: GameSession, turn: TurnRecord) -> TurnRecord:
    raise NotImplementedError

def action_load_bullet(game: GameSession, turn: TurnRecord) -> TurnRecord:
    raise NotImplementedError

def process_response_of_player(game: GameSession,
                               player: Player,
                               turn: TurnRecord) -> TurnRecord:
    response = turn.received_response or "/"
    match response[0]:
        case ActionOfBot.FIRE.value:
            action = action_fire
        case ActionOfBot.MOVE.value:
            action = action_move
        case ActionOfBot.REFUEL.value:
            action = action_refuel
        case ActionOfBot.TOOLS:
            action = action_tools
        case ActionOfBot.SHIELD:
            action = action_change_status_shield
        case ActionOfBot.LOAD:
            action = action_load_bullet
        case other:
            action = action_skip_turn
    executed_turn = action(game=game, turn=turn)
    # TODO: Update player status
    save_doc(db=Databases.TURNS, document=executed_turn)
    return executed_turn


def execute_loop(game: GameSession) -> Player:
    game.current_turn = 0
    while not game.winner:
        game_after_play = game
        for player in game.current_players:
            player_turn = play_next_turn(game)
            game_after_play = process_response_of_player(game, player, player_turn)
            if len(game_after_play.current_players) == 1:
                game_after_play.winner = list(game_after_play.current_players)[0]
                break
            register_event(game_after_play, GameEventType.END_ROUND)
        game = game_after_play               
        if game.current_turn > NORMAL_SIZE_LIMIT:
            reduce_board_size(game)
        save_doc(Databases.GAMES, game)
    return game.winner
            

def get_events(game: GameSession) -> list[GameEvent]:
    ...


def play() -> Player:  # return winner
    all_players = _get_all_players()
    game, ongoing = start_new_game(players = all_players, width=100, height=100)
    if not ongoing:
        randomize_positions(all_players)
    winner = execute_loop(game)
    events = get_events(game)
    return {"winner": winner, "events": events}
