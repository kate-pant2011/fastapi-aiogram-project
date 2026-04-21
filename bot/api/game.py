import httpx
from bot.config import settings, APIError, parse_error
from bot.utils.http_client import client
from datetime import datetime

BASE_URL = settings.BASE_URL


async def get_active_games(tg_id: int) -> dict | None:
    try:
        response = await client.get(f"/games", params={"tg_id": tg_id})

    except httpx.RequestError:
        raise APIError("Server unavailable", 503)

    if response.status_code >= 400:
        message, payload = parse_error(response)
        raise APIError(message, response.status_code, payload)

    return response.json()


async def get_game_in_action(tg_id: int) -> dict | None:
    try:
        response = await client.get(
            f"/games",
            params={"tg_id": tg_id, "status": "in_action"},
        )

    except httpx.RequestError:
        raise APIError("Server unavailable", 503)

    if response.status_code >= 400:
        message, payload = parse_error(response)
        raise APIError(message, response.status_code, payload)

    return response.json()


async def add_new_game(tg_id: int, name: str, start_time: datetime):
    try:
        response = await client.post(
            f"/games", 
            params={"tg_id": tg_id},
            json={"name": name, "start_time":start_time}
        )

    except httpx.RequestError:
        raise APIError("Server unavailable", 503)

    if response.status_code >= 400:
        message, payload = parse_error(response)
        raise APIError(message, response.status_code, payload)

    return response.json()


async def join_game(tg_id: int, game_id: int):
    try:
        response = await client.post(f"/games/{game_id}/join", params={"tg_id": tg_id})

    except httpx.RequestError:
        raise APIError("Server unavailable", 503)

    if response.status_code >= 400:
        message, payload = parse_error(response)
        raise APIError(message, response.status_code, payload)

    return response.json()


async def leave_game(tg_id: int, game_id: int):
    try:
        response = await client.post(f"/games/{game_id}/leave", params={"tg_id": tg_id})

    except httpx.RequestError:
        raise APIError("Server unavailable", 503)

    if response.status_code >= 400:
        message, payload = parse_error(response)
        raise APIError(message, response.status_code, payload)

    return response.json()


async def start_game_api(tg_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/games/start", params={"tg_id": tg_id})

    resp.raise_for_status()
    return resp.json()


async def get_my_games_api(tg_id: int, organizer_id):
    try:
        response = await client.get(
            f"/games", params={"tg_id": tg_id, "organizer_tg_id": organizer_id}
        )

    except httpx.RequestError:
        raise APIError("Server unavailable", 503)

    if response.status_code >= 400:
        message, payload = parse_error(response)
        raise APIError(message, response.status_code, payload)

    return response.json()


async def distribute_tables_api(game_id, tg_id):
    try:
        response = await client.post(f"/games/{game_id}/distribute-tables", params={"tg_id": tg_id})

    except httpx.RequestError:
        raise APIError("Server unavailable", 503)

    if response.status_code >= 400:
        message, payload = parse_error(response)
        raise APIError(message, response.status_code, payload)

    return response.json()
