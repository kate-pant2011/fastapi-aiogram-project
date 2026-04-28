import httpx
from bot.config import settings, APIError, parse_error
from bot.utils.http_client import client
from datetime import datetime

BASE_URL = settings.BASE_URL

async def get_tgchats(tg_id: int):
    try:
        response = await client.get("/tgchats", params={"tg_id": tg_id})

    except httpx.RequestError:
        raise APIError("Server unavailable", 503)

    if response.status_code >= 400:
        message, payload = parse_error(response)
        raise APIError(message, response.status_code, payload)

    return response.json()


async def add_new_tgchat(tg_id: int, chat_title: str, chat_id: int, thread_id: int):
    try:
        response = await client.post(
            f"/tgchats", 
            params={"tg_id": tg_id},
            json={"chat_id": chat_id, "thread_id": thread_id, "chat_title": chat_title}
        )

    except httpx.RequestError:
        raise APIError("Server unavailable", 503)

    if response.status_code >= 400:
        message, payload = parse_error(response)
        raise APIError(message, response.status_code, payload)

    return response.json()

