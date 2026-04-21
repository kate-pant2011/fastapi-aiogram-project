from fastapi import FastAPI
import app.models_loader
import logging
from logging.handlers import RotatingFileHandler
from .middleware import log_requests
from app.routers.table_player import table_player_router
from app.routers.player import player_router
from app.routers.score import elo_router
from app.routers.table import table_router
from app.routers.game import game_router

app = FastAPI()

app.middleware("http")(log_requests)

app.include_router(table_player_router)
app.include_router(player_router)
app.include_router(elo_router)
app.include_router(table_router)
app.include_router(game_router)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

handler = RotatingFileHandler(
    "app.log",
    maxBytes=1_000_000,
    backupCount=3
)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)