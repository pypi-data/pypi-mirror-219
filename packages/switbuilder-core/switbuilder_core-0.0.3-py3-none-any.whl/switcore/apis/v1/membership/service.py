from action.schemas import ActionRequest
from membership.schemas import OrganizationUser
from membership.utils import get_org_user_list_url


async def get_all_org_users(
        action_request: ActionRequest,
        workspace_id: str,
) -> list[OrganizationUser]:
    param = {
        'filters.membership_status': 'active',
        'ws_id': workspace_id,
    }
    res = await action_request.swit_client.get(get_org_user_list_url())

    data: dict = res.json()
    data = data.get('data', {})

    users_data: list[dict] = data.get('users', [])
    return [OrganizationUser(**user) for user in users_data]
