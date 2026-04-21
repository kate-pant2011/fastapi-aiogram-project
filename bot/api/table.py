import httpx
from bot.config import settings, APIError, parse_error
from bot.utils.http_client import client
from datetime import datetime

BASE_URL = settings.BASE_URL


async def join_table(tg_id: int, table_id: int):
    try:
        response = await client.post(f"/tables/{table_id}/players", params={"tg_id": tg_id})

    except httpx.RequestError:
        raise APIError("Server unavailable", 503)

    if response.status_code >= 400:
        message, payload = parse_error(response)
        raise APIError(message, response.status_code, payload)

    return response.json()


async def get_tables(tg_id: int, game_id: int):
    try:
        response = await client.get(f"/games/{game_id}/tables", params={"tg_id": tg_id})

    except httpx.RequestError:
        raise APIError("Server unavailable", 503)

    if response.status_code >= 400:
        message, payload = parse_error(response)
        raise APIError(message, response.status_code, payload)

    return response.json()


async def close_table(tg_id: int, table_id: int) -> dict:
    try:
        response = await client.post(f"/tables/{table_id}/close", params={"tg_id": tg_id})

    except httpx.RequestError:
        raise APIError("Server unavailable", 503)

    if response.status_code >= 400:
        message, payload = parse_error(response)
        raise APIError(message, response.status_code, payload)

    return response.json()


async def get_my_table(tg_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BASE_URL}/tables/me",
            params={"tg_id": tg_id},
        )

    r.raise_for_status()
    return r.json()


async def get_my_table_api(tg_id: int):
    try:
        response = await client.get(
            "/players/me/table",
            params={
                "tg_id": tg_id,
            },
        )

    except httpx.RequestError:
        raise APIError("Server unavailable", 503)

    if response.status_code >= 400:
        message, payload = parse_error(response)
        raise APIError(message, response.status_code, payload)

    return response.json()


async def set_player_chips_api(tg_id: int, player_id: int, table_id: int, chips: int):
    try:
        response = await client.patch(
            f"/tables/{table_id}/players/{player_id}",
            params={"tg_id": tg_id},
            json={"chips": chips},
        )

    except httpx.RequestError:
        raise APIError("Server unavailable", 503)

    if response.status_code >= 400:
        message, payload = parse_error(response)
        raise APIError(message, response.status_code, payload)

    return response.json()


async def knockout_player_api(tg_id: int, table_id: int, player_id: int):
    try:
        response = await client.post(
            f"/tables/{table_id}/players/{player_id}/finish",
            params={"tg_id": tg_id},
            json={"eliminated": True, "chips": 0},
        )

    except httpx.RequestError:
        raise APIError("Server unavailable", 503)

    if response.status_code >= 400:
        message, payload = parse_error(response)
        raise APIError(message, response.status_code, payload)

    return response.json()
