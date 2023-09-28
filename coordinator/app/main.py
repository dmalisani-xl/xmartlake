import logging
from fastapi import (
    FastAPI,
    status,
    HTTPException,
)
from app.models import PlayerLoader
from app.rpc.grpc_main import build_image, call_to_bot, ping_to_builder, ping_to_manager
from app.game import play, register_new_player, find_existent_bot

log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger = logging.getLogger(__name__)
logger.addHandler(log_handler)
logger.setLevel(logging.DEBUG)

VERSION = "0.0.1"


app = FastAPI(
    title="XmartLake coordinator",
    description=f"API for the botgame",
    version=VERSION
)

@app.get("/")
async def root():
    return {"message": f"XmartLake coordinatior works!. Version: {VERSION}"}


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(body: PlayerLoader):
    exist, same_email = find_existent_bot(
        bot_id=body.bot_identifier,
        email=body.email
    )
    if exist and not same_email:
        raise HTTPException(f"Identifier {body.bot_identifier} already exists")

    logger.debug(f"Building {body.bot_identifier}")
    image_id = build_image(bot_id=body.bot_identifier, language=body.language, code=body.code)
    register_new_player(body, image_id)
    return image_id

@app.get("/call")
async def call(bot_id: str, parameter: str):
    return call_to_bot(bot_id, parameter)


@app.get("/ping-builder")
async def ping_builder():
    return ping_to_builder()


@app.get("/ping-manager")
async def ping_manager():
    return ping_to_manager()

@app.get("/play")
async def playgame():
    try:
        return play()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args[0])
