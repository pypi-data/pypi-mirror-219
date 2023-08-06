import logging

from switcore.apis.v1.conversation.schemas import Room

logger = logging.getLogger()


async def get_all_rooms_recursive(
        action_request: ActionRequest,
        offset: str | None = None) -> list[Room]:
    params: dict = {
        "limit": 50,
    }

    if offset:
        params["offset"] = offset

    res = await action_request.swit_client.get(get_rooms_url(), params=params)

    data: dict = res.json()
    data = data.get('data', {})

    rooms_data: list[dict] = data.get('rooms', [])
    offset: str | None = data.get('offset', None)

    if len(rooms_data) == 0:
        return []

    rooms = [Room(**room) for room in rooms_data]
    next_rooms = await get_all_rooms_recursive(action_request, offset)
    return rooms + next_rooms


async def get_all_rooms(action_request: ActionRequest) -> list[Room]:
    res = await action_request.swit_client.get(get_rooms_url())

    data: dict = res.json()
    data = data.get('data', {})

    rooms_data: list[dict] = data.get('rooms', [])
    return [Room(**room) for room in rooms_data]
