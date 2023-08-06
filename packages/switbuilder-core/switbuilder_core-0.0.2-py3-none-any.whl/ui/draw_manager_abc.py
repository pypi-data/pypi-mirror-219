from abc import ABC, abstractmethod, ABCMeta

from action.constants import ViewIdTypes
from action.schemas import SwitRequest, State
from ui.swit_response.SwitResponse import SwitResponse, ViewCallbackType
from ui.swit_response.View import View


class DrawManagerABC(ABC):

    def __init__(self,
                 swit_request: SwitRequest,
                 state: State,
                 view_call_back_type: ViewCallbackType,
                 view_id: ViewIdTypes,
                 reference_view_id: ViewIdTypes | None = None,
                 new_state_data: dict | None = None
                 ):
        self.swit_request = swit_request
        self.state = state
        self.view_call_back_type = view_call_back_type
        self.view_id = view_id
        self.reference_view_id = reference_view_id
        if new_state_data:
            self.state = self.state.update(new_state_data)

    @abstractmethod
    async def draw(self) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def build_view(self) -> View:
        raise NotImplementedError()
