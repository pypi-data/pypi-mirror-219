from action.schemas import ActionRequest
from ui.swit_response.SwitResponse import ViewCallbackType


def update_to_current_view(action_request: ActionRequest):
    assert action_request.current_view, "action_request must have current_view"
    return ViewCallbackType.update, action_request.current_view.view_id

