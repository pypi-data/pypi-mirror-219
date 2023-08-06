from action.activity_handler_abc import ActivityHandlerABC
from action.constants import ViewIdTypes, ActionIdTypes, init_state
from action.schemas import State, ActionRequest, UserActionType
from auth import service as auth_service
from auth.exception import SwitNeedScopeException
from auth.repository import UserRepository
from imap.exception import EmailFetchFailedException, InvalidConnectionException
from ui.draw_managers import SignInDrawManager, MailListDrawManager, BackToMailListDrawManager, \
    ShareModalDrawManager, WorkspaceChangeModalDrawManager, ChannelChangeModalDrawManager, MailDetailDrawManager, \
    LogoutModalDrawManager, MailListFromStateDrawManager, ShareCloseDrawManager
from ui.service import update_to_current_view
from ui.swit_response.SwitResponse import SwitResponse, ViewCallbackType
from ui.view_draw_managers.attach_to_task_modal import draw_manager as attach_to_task_modal_draw_manager
from ui.view_draw_managers.convert_to_task_modal import draw_manager as convert_to_task_modal_draw_manager
from ui.view_draw_managers.need_authorization_modal import draw_manager as need_authorization_modal_draw_manager
from ui.view_draw_managers.share_to_dm_modal import draw_manager as share_to_dm_modal_draw_manager


class ActivityHandler(ActivityHandlerABC):

    def __init__(self, action_request: ActionRequest, state: State):
        super().__init__(action_request, state)
        self.action_request = action_request

    async def on_turn(self) -> SwitResponse:
        if self.action_request.user_action.type == UserActionType.view_actions_drop:
            response = await self.on_view_actions_drop()
        elif self.action_request.user_action.type == UserActionType.view_actions_submit:
            response = await self.on_view_actions_submit()
        elif self.action_request.user_action.type == UserActionType.right_panel_open:
            response = await self.on_right_panel_open()
        elif self.action_request.user_action.type == UserActionType.view_actions_input:
            response = await self.on_view_actions_input()
        elif self.action_request.user_action.type == UserActionType.view_actions_oauth_complete:
            response = await self.on_view_actions_oauth_complete()
        elif self.action_request.user_action.type == UserActionType.user_commands_chat_extension:
            response = await self.on_user_commands_chat_extension()
        elif self.action_request.user_action.type == UserActionType.user_commands_chat:
            response = await self.on_user_commands_chat()
        else:
            assert False, "undefined user_action type"

        return response

    async def on_right_panel_open(self) -> SwitResponse:
        new_state_data = {'workspace_id': self.action_request.context.workspace_id}
        callback_type = ViewCallbackType.initialize
        view_id = ViewIdTypes.right_panel
        try:
            response = await MailListDrawManager(
                self.action_request,
                self.state,
                callback_type,
                view_id,
                new_state_data=new_state_data
            ).draw()
        except (EmailFetchFailedException, InvalidConnectionException, SwitNeedScopeException) as e:
            UserRepository(self.action_request.session).delete(self.action_request.user.swit_id)
            response = await SignInDrawManager(
                self.action_request,
                self.state,
                callback_type,
                view_id,
                new_state_data=new_state_data
            ).draw()

        return response

    async def on_presence_sync(self) -> SwitResponse:
        pass

    async def on_user_commands_chat(self) -> SwitResponse:
        new_state_data = {"workspace_id": self.action_request.context.workspace_id,
                          "channel_id": self.action_request.context.channel_id}
        callback_type = ViewCallbackType.open
        view_id = ViewIdTypes.user_command_modal

        try:
            response = await MailListDrawManager(
                self.action_request,
                self.state,
                callback_type,
                view_id,
                new_state_data=new_state_data
            ).draw()
            return response
        except (EmailFetchFailedException, InvalidConnectionException) as e:
            UserRepository(self.action_request.session).delete(self.action_request.user.swit_id)
            response = await SignInDrawManager(
                self.action_request,
                self.state,
                callback_type,
                view_id,
                new_state_data=new_state_data
            ).draw()
        return response

    async def on_user_commands_chat_extension(self) -> SwitResponse:
        new_state_data = {"workspace_id": self.action_request.context.workspace_id,
                          "channel_id": self.action_request.context.channel_id}
        callback_type = ViewCallbackType.open
        view_id = ViewIdTypes.user_command_modal

        try:
            response = await MailListDrawManager(
                self.action_request,
                self.state,
                callback_type,
                view_id,
                new_state_data=new_state_data
            ).draw()
            return response
        except (EmailFetchFailedException, InvalidConnectionException) as e:
            UserRepository(self.action_request.session).delete(self.action_request.user.swit_id)
            response = await SignInDrawManager(
                self.action_request,
                self.state,
                callback_type,
                view_id,
                new_state_data=new_state_data
            ).draw()

        return response

    async def on_user_commands_chat_commenting(self) -> SwitResponse:
        pass

    async def on_user_commands_context_menus_message(self) -> SwitResponse:
        pass

    async def on_user_commands_context_menus_message_comment(self) -> SwitResponse:
        pass

    async def on_view_actions_drop(self) -> SwitResponse:
        response = await ShareModalDrawManager(
            self.action_request,
            self.state,
            ViewCallbackType.open,
            ViewIdTypes.share_modal,
            new_state_data={"shared_email_id": self.action_request.user_action.id}
        ).draw()
        return response

    async def on_view_actions_input(self) -> SwitResponse:
        user_action: str = self.action_request.user_action.id

        if ActionIdTypes.search in user_action:
            keyword: str = (self.action_request.current_view.body.elements[0].value
                            or self.action_request.user_action.value)
            response = await MailListDrawManager(
                self.action_request,
                self.state,
                *update_to_current_view(self.action_request),
                new_state_data={"keyword": keyword, "seq": init_state["seq"], "limit": init_state["limit"]}
            ).draw()
        elif ActionIdTypes.select_workspace_on_share_modal in user_action:
            response = await WorkspaceChangeModalDrawManager(
                self.action_request,
                self.state,
                *update_to_current_view(self.action_request)
            ).draw()
        elif ActionIdTypes.select_channel_on_share_modal in user_action:
            response = await ChannelChangeModalDrawManager(
                self.action_request,
                self.state,
                *update_to_current_view(self.action_request)
            ).draw()
        elif ActionIdTypes.select_workspace_on_convert_new_task_modal in user_action:
            response = await convert_to_task_modal_draw_manager.WorkspaceChangeDrawManager(
                self.action_request,
                self.state,
                *update_to_current_view(self.action_request)
            ).draw()
        elif ActionIdTypes.select_workspace_on_attach_new_task_modal in user_action:
            response = await attach_to_task_modal_draw_manager.WorkspaceChangeDrawManager(
                self.action_request,
                self.state,
                *update_to_current_view(self.action_request)
            ).draw()
        elif ActionIdTypes.select_project_on_convert_new_task_modal in user_action:
            response = await convert_to_task_modal_draw_manager.ProjectChangeDrawManager(
                self.action_request,
                self.state,
                *update_to_current_view(self.action_request)
            ).draw()
        elif ActionIdTypes.select_project_on_attach_task_modal in user_action:
            response = await attach_to_task_modal_draw_manager.ProjectChangeDrawManager(
                self.action_request,
                self.state,
                *update_to_current_view(self.action_request)
            ).draw()
        elif ActionIdTypes.select_task_on_attach_task_modal in user_action:
            response = await attach_to_task_modal_draw_manager.TaskChangeDrawManager(
                self.action_request,
                self.state,
                *update_to_current_view(self.action_request)
            ).draw()
        elif ActionIdTypes.select_room_on_share_to_dm_modal in user_action:
            response = await share_to_dm_modal_draw_manager.RoomChangeDrawManager(
                self.action_request,
                self.state,
                *update_to_current_view(self.action_request)
            ).draw()
        elif ActionIdTypes.select_label in user_action:
            response = await MailListDrawManager(
                self.action_request,
                self.state,
                *update_to_current_view(self.action_request),
                new_state_data={"label": ActionIdTypes.get_action_value(self.action_request.user_action.id),
                                "seq": init_state["seq"],
                                "limit": init_state["limit"]}
            ).draw()
        else:
            assert False, "undefined input_command!!"

        return response

    async def on_view_actions_submit(self) -> SwitResponse:
        assert self.action_request.current_view, "current_view가 있어야함!!"
        user_action: str = self.action_request.user_action.id
        view_id: ViewIdTypes = self.action_request.current_view.view_id

        if ActionIdTypes.go_to_mail_detail in user_action:
            response = await MailDetailDrawManager(
                self.action_request,
                self.state,
                *update_to_current_view(self.action_request)
            ).draw()
        elif ActionIdTypes.back_to_mail_list in user_action:
            response = await BackToMailListDrawManager(
                self.action_request,
                self.state,
                *update_to_current_view(self.action_request)
            ).draw()
        elif ActionIdTypes.open_logout_modal_from_right_panel in user_action:
            response = await LogoutModalDrawManager(
                self.action_request,
                self.state,
                ViewCallbackType.open,
                ViewIdTypes.logout_modal
            ).draw()
        elif ActionIdTypes.open_convert_to_task_modal in user_action:
            response = await convert_to_task_modal_draw_manager.ConvertTaskModalDrawManager(
                self.action_request,
                self.state,
                ViewCallbackType.open,
                ViewIdTypes.convert_to_task_modal
            ).draw()
        elif ActionIdTypes.open_attach_to_task_modal in user_action:
            response = await attach_to_task_modal_draw_manager.AttachTaskModalDrawManager(
                self.action_request,
                self.state,
                ViewCallbackType.open,
                ViewIdTypes.attach_to_task_modal
            ).draw()
        elif ActionIdTypes.open_share_to_dm_modal in user_action:
            response = await share_to_dm_modal_draw_manager.ShareDmModalDrawManager(
                self.action_request,
                self.state,
                ViewCallbackType.open,
                ViewIdTypes.attach_to_task_modal
            ).draw()
        elif ActionIdTypes.open_logout_modal_from_action_modal in user_action:
            response = await LogoutModalDrawManager(
                self.action_request,
                self.state,
                *update_to_current_view(self.action_request),
                new_state_data={"email_list_view": self.action_request.current_view.dict()}
            ).draw()
        elif ActionIdTypes.close_logout_modal in user_action:
            response = await MailListFromStateDrawManager(
                self.action_request,
                self.state,
                *update_to_current_view(self.action_request),
            ).draw()
        elif ActionIdTypes.close_need_scope_modal in user_action:
            response = await need_authorization_modal_draw_manager.PrevViewDrawManager(
                self.action_request, self.state, *update_to_current_view(self.action_request)
            ).draw()
        elif ActionIdTypes.logout_from_right_panel in user_action:
            await auth_service.delete(self.action_request.user, self.action_request.session)
            new_state = self.state.refresh()
            response = await SignInDrawManager(
                self.action_request,
                new_state,
                ViewCallbackType.update,
                ViewIdTypes.right_panel,
                ViewIdTypes.right_panel
            ).draw()
        elif ActionIdTypes.logout_from_modal in user_action:
            await auth_service.delete(self.action_request.user, self.action_request.session)
            new_state = self.state.refresh()
            response = await SignInDrawManager(
                self.action_request,
                new_state,
                *update_to_current_view(self.action_request)
            ).draw()
        elif ActionIdTypes.refresh in user_action:
            response = await MailListDrawManager(
                self.action_request,
                self.state.refresh(),
                *update_to_current_view(self.action_request)
            ).draw()
        elif ActionIdTypes.next_page in user_action:
            new_state = self.state.update({"seq": self.state.seq + self.state.limit})
            response = await MailListDrawManager(
                self.action_request,
                new_state,
                *update_to_current_view(self.action_request)
            ).draw()
        elif ActionIdTypes.prev_page in user_action:
            new_state = self.state.update({"seq": self.state.seq - self.state.limit})
            response = await MailListDrawManager(
                self.action_request,
                new_state,
                *update_to_current_view(self.action_request)
            ).draw()
        elif ActionIdTypes.share_to_channel_from_action_modal in user_action:
            response = await ShareModalDrawManager(
                self.action_request,
                self.state,
                *update_to_current_view(self.action_request),
                new_state_data={"shared_email_id": self.action_request.user_action.id}
            ).draw()

        elif ActionIdTypes.share_to_channel_from_detail in user_action:
            response = await ShareModalDrawManager(
                self.action_request,
                self.state,
                ViewCallbackType.open,
                ViewIdTypes.share_modal,
                new_state_data={"shared_email_id": self.action_request.user_action.id}
            ).draw()
        elif ActionIdTypes.share_and_close_modal in user_action:
            response = await ShareCloseDrawManager(
                self.action_request,
                self.state,
                *update_to_current_view(self.action_request)
            ).draw()
        elif ActionIdTypes.convert_to_new_task in user_action:
            response = await convert_to_task_modal_draw_manager.ConvertCloseModalDrawManager(
                self.action_request,
                self.state,
                ViewCallbackType.close,
                self.action_request.current_view.view_id
            ).draw()
        elif ActionIdTypes.attach_to_task in user_action:
            response = await attach_to_task_modal_draw_manager.AttachCloseModalDrawManager(
                self.action_request,
                self.state,
                ViewCallbackType.close,
                self.action_request.current_view.view_id
            ).draw()
        elif ActionIdTypes.share_to_dm in user_action:
            response = await share_to_dm_modal_draw_manager.ShareCloseModalDrawManager(
                self.action_request,
                self.state,
                ViewCallbackType.close,
                self.action_request.current_view.view_id
            ).draw()
        else:
            assert False, "undefined submit action!!"
        return response

    async def on_view_actions_oauth_complete(self) -> SwitResponse:
        if self.state.prev_view:
            response = SwitResponse(
                callback_type=ViewCallbackType.close,
                new_view=self.action_request.current_view)

            # TODO 403 공통화!
            # if self.action_request.current_view.view_id == ViewIdTypes.right_panel:
            #     response = SwitResponse(
            #         callback_type=ViewCallbackType.close,
            #         new_view=self.action_request.current_view
            #     )
            # else:
            #     response = await PrevViewDrawManager(
            #         self.action_request,
            #         self.state,
            #         *update_to_current_view(self.action_request)
            #     ).draw()

            return response

        try:
            response = await MailListDrawManager(
                self.action_request,
                self.state,
                *update_to_current_view(self.action_request)
            ).draw()
            return response
        except (EmailFetchFailedException, InvalidConnectionException) as e:
            UserRepository(self.action_request.session).delete(self.action_request.user.swit_id)
            response = await SignInDrawManager(
                self.action_request,
                self.state,
                *update_to_current_view(self.action_request)
            ).draw()
        return response
