from fastapi import (
    FastAPI,
    status
)
from app.models import PlayerLoader

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
    ...

@app.get("/x")
def prueba():
    from app.game import play
    play()
