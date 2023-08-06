from abc import ABC, abstractmethod
from collections import defaultdict

from switcore.action.activity_router import ActivityRouter, PathResolver
from switcore.action.schemas import SwitRequest, State, SwitResponse, UserActionType
from switcore.type import DrawerHandler


class ActivityHandlerABC(ABC):
    def __init__(self) -> None:
        self.handler: dict[str, dict[str, DrawerHandler]] = defaultdict(dict)

    def include_activity_router(self, activity_router: ActivityRouter):
        for view_id, _dict in activity_router.handler.items():
            for action_id, func in _dict.items():
                self.handler[view_id][action_id] = func

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

    async def on_view_actions_submit(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        user_action: str = swit_request.user_action.id
        action_id_path_resolver: PathResolver = PathResolver.from_combined(user_action)
        view_id_path_resolver: PathResolver = PathResolver.from_combined(swit_request.current_view.view_id)

        drawer_func_or_null: DrawerHandler | None = (
            self.handler
            .get(view_id_path_resolver.id, {})
            .get(action_id_path_resolver.id, None))

        assert drawer_func_or_null, f"undefined submit action!!: {user_action}"

        args = [swit_request, state, *action_id_path_resolver.paths]
        response = await drawer_func_or_null(*args)
        return response

    @abstractmethod
    async def on_view_actions_oauth_complete(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        raise NotImplementedError()
