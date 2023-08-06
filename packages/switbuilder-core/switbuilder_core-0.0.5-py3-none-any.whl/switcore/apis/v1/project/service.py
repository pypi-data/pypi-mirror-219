from action.schemas import ActionRequest
from project.schemas import Project
from project.utils import get_projects_url


def get_project_or_null(projects: list[Project], project_id: str) -> Project | None:
    ret = None
    for project in projects:
        if project.id == project_id:
            ret = project
            break

    return ret


async def get_all_projects_recursive(
        action_request: ActionRequest,
        workspace_id: str,
        offset: str | None = None
) -> list[Project]:
    params: dict = {
        "limit": 50,
        "workspace_id": workspace_id,
    }

    if offset:
        params["offset"] = offset

    res = await action_request.swit_client.get(get_projects_url(), params=params)

    data: dict = res.json()
    data = data.get('data', {})

    projects_data: list[dict] = data.get('projects', [])
    offset: str | None = data.get('offset', None)

    if len(projects_data) == 0:
        return []

    projects = [Project(**project) for project in projects_data]
    next_projects = await get_all_projects_recursive(action_request, workspace_id, offset)
    return projects + next_projects
