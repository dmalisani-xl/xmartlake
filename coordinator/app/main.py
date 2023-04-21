from fastapi import (
    FastAPI,
    status,
    HTTPException
)
from app.models import PlayerLoader
from app.rpc.grpc_main import build_image, call_to_bot, ping_to_builder, ping_to_manager
from app.game import play
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
    return build_image(bot_id=body.bot_identifier, language=body.language, code=body.code)

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
