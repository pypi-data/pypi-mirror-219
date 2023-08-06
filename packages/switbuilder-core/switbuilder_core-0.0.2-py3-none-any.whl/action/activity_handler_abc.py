from abc import ABC, abstractmethod

from action.schemas import SwitRequest, State
from ui.swit_response.SwitResponse import SwitResponse


class ActivityHandlerABC(ABC):
    def __init__(self, swit_request: SwitRequest, state: State):
        self.swit_request = swit_request
        self.state = state
        self.state.is_valid()

    @abstractmethod
    async def on_turn(self) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_right_panel_open(self) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_presence_sync(self) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_user_commands_chat(self) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_user_commands_chat_extension(self) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_user_commands_chat_commenting(self) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_user_commands_context_menus_message(self) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_user_commands_context_menus_message_comment(self) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_view_actions_drop(self) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_view_actions_input(self) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_view_actions_submit(self) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_view_actions_oauth_complete(self) -> SwitResponse:
        raise NotImplementedError()
