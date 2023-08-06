from schemas import Channel
from switcore.action.schemas import SwitRequest
from switcore.apis.v1.channel.utils import get_channels_url


def get_channel_or_null(channels: list[Channel], channel_id: str) -> Channel | None:
    ret = None
    for channel in channels:
        if channel.id == channel_id:
            ret = channel
            break

    return ret


async def get_all_channels_recursive(
        action_request: SwitRequest,
        workspace_id: str,
        offset: str | None = None
) -> list[Channel]:
    params: dict = {
        "limit": 50,
        "workspace_id": workspace_id,
    }

    if offset:
        params["offset"] = offset

    res = await action_request.swit_client.get(get_channels_url(), params=params)

    data: dict = res.json()
    data = data.get('data', {})

    channels_data: list[dict] = data.get('channels', [])
    offset: str | None = data.get('offset', None)

    if len(channels_data) == 0:
        return []

    channels = [Channel(**channel) for channel in channels_data]
    next_channels = await get_all_channels_recursive(action_request, workspace_id, offset)
    return channels + next_channels
