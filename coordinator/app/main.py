from fastapi import (
    FastAPI,
    status
)
from app.models import PlayerLoader

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

@app.get("/x")
def prueba():
    from game import decode_environment
    # payload = '/..../..../.X../..F./..F.'
    payload = 'F2345/2345/2345/234F/23F5HABIAUNAVEZ'
    print(decode_environment(payload))