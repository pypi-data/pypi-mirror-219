import logging

from action.schemas import ActionRequest
from workspace.schemas import Workspace
from workspace.utils import get_workspaces_url

logger = logging.getLogger()


def get_workspace(workspaces: list[Workspace], workspace_id: str) -> Workspace:
    ret = None
    for workspace in workspaces:
        if workspace.id == workspace_id:
            ret = workspace
            break

    assert ret is not None, "invalid workspace_id"
    return ret


async def get_all_workspaces_recursive(
        action_request: ActionRequest,
        offset: str | None = None) -> list[Workspace]:
    params: dict = {
        "limit": 50,
    }

    if offset:
        params["offset"] = offset

    res = await action_request.swit_client.get(get_workspaces_url(), params=params)

    data: dict = res.json()
    data = data.get('data', {})

    workspaces_data: list[dict] = data.get('workspaces', [])
    offset: str | None = data.get('offset', None)

    if len(workspaces_data) == 0:
        return []

    workspaces = [Workspace(**workspace) for workspace in workspaces_data]
    next_workspaces = await get_all_workspaces_recursive(action_request, offset)
    return workspaces + next_workspaces
