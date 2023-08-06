from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from action.activity_handler import ActivityHandler
from action.constants import init_state
from action.schemas import ActionRequest, State
from auth.dependencies import get_user, get_swit_http_client
from auth.oauth2 import SwitHttpClient
from auth.schemas import UserSchema
from database import get_db_session


async def get_action_request(
        request: Request,
        user: UserSchema = Depends(get_user),
        session: Session = Depends(get_db_session),
        swit_client: SwitHttpClient = Depends(get_swit_http_client)
):
    res: dict = await request.json()
    if not swit_client.swit_request.current_view:
        res['current_view'] = None

    return ActionRequest(origin_reqeust=request, user=user, session=session, swit_client=swit_client, **res)


async def get_state(action_request: ActionRequest = Depends(get_action_request)) -> State:
    current_view = action_request.current_view
    if current_view is None:
        return State(**{**init_state})
    return State.from_bytes(current_view.state)


def get_activity_handler(
        action_request: ActionRequest = Depends(get_action_request),
        state: State = Depends(get_state)) -> ActivityHandler:
    return ActivityHandler(action_request, state)
