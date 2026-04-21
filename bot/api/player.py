import httpx
from bot.config import settings, APIError, parse_error
from bot.utils.http_client import client

BASE_URL = settings.BASE_URL

async def register_player(tg_id: int, name: str):
    try:
        response = await client.post(
            f"/players/tg/{tg_id}",
            json={"name": name},
        )

    except httpx.RequestError:
        raise APIError("Server unavailable", 503)

    if response.status_code >= 400:
        message, payload = parse_error(response)
        raise APIError(message, response.status_code, payload)


    return response.json()


async def get_leaderboard(tg_id: int, limit: int = 20):
    try:
        response = await client.get(
            "/players/leaderboard",
            params={
                "tg_id": tg_id,
                "limit": limit
            }
        )
        
    except httpx.RequestError:
        raise APIError("Server unavailable", 503)

    if response.status_code >= 400:
        message, payload = parse_error(response)
        raise APIError(message, response.status_code, payload)


    return response.json()
    

async def get_player_stats(tg_id: int):
    try:
        response = await client.get(
            f"/players/me",
            params={"tg_id": tg_id}
        )

    except httpx.RequestError:
        raise APIError("Server unavailable", 503)

    if response.status_code >= 400:
        message, payload = parse_error(response)
        raise APIError(message, response.status_code, payload)


    return response.json()