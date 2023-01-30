from fastapi import (
    FastAPI,
    status
)
from models import PlayerLoader

VERSION = "0.0.1"
app = FastAPI(
    title="boXLike coordinator",
    description=f"API for the botgame",
    version=VERSION
)

@app.get("/")
async def root():
    return {"message": f"BoXLike coordinatior works!. Version: {VERSION}"}


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(body: PlayerLoader):
    ...