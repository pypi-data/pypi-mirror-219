from fastapi import Depends
from starlette.requests import Request

from switcore.action.schemas import SwitRequest, State


async def get_swit_request(
        request: Request,
):
    res: dict = await request.json()
    return SwitRequest(**res)


async def get_state(swit_request: SwitRequest = Depends(get_swit_request)) -> State:
    current_view = swit_request.current_view
    if current_view is None:
        return State.init()
    return State.from_bytes(current_view.state)
