from abc import ABC, abstractmethod

from src.action.activity_router import ActivityRouter
from src.action.schemas import SwitRequest, State, UserActionType, SwitResponse


class ActivityHandlerABC(ABC):

    async def on_turn(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        if swit_request.user_action.type == UserActionType.view_actions_drop:
            response = await self.on_view_actions_drop(swit_request, state)
        elif swit_request.user_action.type == UserActionType.view_actions_submit:
            response = await self.on_view_actions_submit(swit_request, state)
        elif swit_request.user_action.type == UserActionType.right_panel_open:
            response = await self.on_right_panel_open(swit_request, state)
        elif swit_request.user_action.type == UserActionType.view_actions_input:
            response = await self.on_view_actions_input(swit_request, state)
        elif swit_request.user_action.type == UserActionType.view_actions_oauth_complete:
            response = await self.on_view_actions_oauth_complete(swit_request, state)
        elif swit_request.user_action.type == UserActionType.user_commands_chat_extension:
            response = await self.on_user_commands_chat_extension(swit_request, state)
        elif swit_request.user_action.type == UserActionType.user_commands_chat:
            response = await self.on_user_commands_chat(swit_request, state)
        else:
            assert False, "undefined user_action type"

        return response

    async def include_activity_router(self, activity_router: ActivityRouter):
        raise NotImplementedError()

    @abstractmethod
    async def on_right_panel_open(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_presence_sync(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_user_commands_chat(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_user_commands_chat_extension(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_user_commands_chat_commenting(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_user_commands_context_menus_message(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_user_commands_context_menus_message_comment(self, swit_request: SwitRequest,
                                                             state: State) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_view_actions_drop(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_view_actions_input(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_view_actions_submit(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        raise NotImplementedError()

    @abstractmethod
    async def on_view_actions_oauth_complete(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        raise NotImplementedError()
