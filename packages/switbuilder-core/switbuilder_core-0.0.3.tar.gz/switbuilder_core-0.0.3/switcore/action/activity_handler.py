from collections import defaultdict

from src.action.activity_handler_abc import ActivityHandlerABC
from src.action.activity_router import ActivityRouter, PathResolver
from src.action.schemas import State, SwitRequest, SwitResponse
from src.type import DrawerHandler
from src.webhook_handler.constants import ViewIdTypes, ActionIdTypes


class ActivityHandler(ActivityHandlerABC):

    def __init__(self) -> None:
        self.handler: dict[str, dict[str, DrawerHandler]] = defaultdict(dict)

    def include_activity_router(self, activity_router: ActivityRouter):
        for view_id, _dict in activity_router.handler.items():
            for action_id, func in _dict.items():
                self.handler[view_id][action_id] = func

    async def on_right_panel_open(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        func = self.handler[ViewIdTypes.right_panel][ActionIdTypes.webhook_list]
        return await func(swit_request, state)

    async def on_view_actions_input(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        pass

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

    async def on_view_actions_oauth_complete(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        pass

    async def on_presence_sync(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        pass

    async def on_user_commands_chat(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        pass

    async def on_user_commands_chat_extension(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        pass

    async def on_user_commands_chat_commenting(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        pass

    async def on_user_commands_context_menus_message(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        pass

    async def on_user_commands_context_menus_message_comment(self, swit_request: SwitRequest,
                                                             state: State) -> SwitResponse:
        pass

    async def on_view_actions_drop(self, swit_request: SwitRequest, state: State) -> SwitResponse:
        pass
