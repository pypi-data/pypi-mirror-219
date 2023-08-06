from enum import Enum

init_state: dict = {
    "label": "INBOX",
    "seq": 1,
    "limit": 15,
    "scope": "ALL",
    "keyword": "",
    "search_type": "LATEST",
    "email_list_view": {},
    "email_action_id": "",
    "shared_email_id": "",
    "workspace_id": "",
    "channel_id": "",
    "workspaces": [],
    "channels": [],
    "email_detail_raw": "",
    "email_detail_message_id": "",
    "prev_view": "",
}


class PlatformTypes(str, Enum):
    DESKTOP = 'Desktop'
    IOS = 'iOS'
    ANDROID = 'Android'


class ViewIdTypes(str, Enum):
    right_panel = "right_panel"
    user_command_modal = "user_command_modal"
    share_modal = "share_modal"
    logout_modal = "logout_modal"
    convert_to_task_modal = "convert_to_task_modal"
    attach_to_task_modal = "attach_to_task_modal"
    share_to_dm_modal = "share_to_dm_modal"
    need_authorization_modal = "need_authorization_modal"


class ActionIdTypes(str, Enum):
    next_page = "next_page"
    prev_page = "prev_page"
    go_to_mail_detail = "go_to_mail_detail"
    back_to_mail_list = "back_to_mail_list"
    refresh = "refresh"
    convert_to_new_task = "convert_to_new_task"
    attach_to_task = "attach_to_task"
    logout_from_right_panel = "logout_from_right_panel"
    logout_from_modal = "logout_from_modal"
    open_logout_modal_from_right_panel = "open_logout_modal_from_right_panel"
    open_convert_to_task_modal = "open_convert_to_task_modal"
    open_attach_to_task_modal = "open_attach_to_task_modal"
    open_share_to_dm_modal = "open_share_to_dm_modal"
    open_need_scope_modal = "open_need_scope_modal"
    open_logout_modal_from_action_modal = "open_logout_modal_from_action_modal"
    close_logout_modal = "close_logout_modal"
    close_need_scope_modal = "close_need_scope_modal"
    search = "search"
    download_file = "download_file"
    share_to_channel_from_action_modal = "share_to_channel_from_action_modal"
    share_to_channel_from_detail = "share_to_channel_from_detail"
    share_and_close_modal = "share_and_close_modal"
    select_workspace_on_share_modal = "select_workspace_on_share_modal"
    select_project_on_convert_new_task_modal = "select_project_on_convert_new_task_modal"
    select_workspace_on_convert_new_task_modal = "select_workspace_on_convert_new_task_modal"
    select_room_on_share_to_dm_modal = "select_room_on_share_to_dm_modal"
    select_project_on_attach_task_modal = "select_project_on_attach_task_modal"
    select_workspace_on_attach_new_task_modal = "select_workspace_on_attach_new_task_modal"
    select_task_on_attach_task_modal = "select_task_on_attach_task_modal"
    select_channel_on_share_modal = "select_channel_on_share_modal"
    select_label = "select_label"
    share_to_dm = "share_to_dm"

    @staticmethod
    def get_action_value(user_action: str) -> str:
        fields = [action_type.name for action_type in ActionIdTypes]
        for field in fields:
            if field in user_action:
                return user_action[len(field) + 2:]

        assert False, "get_action_value empty value!!"

    @staticmethod
    def get_action_key(user_action: str) -> str:
        fields = [action_type.name for action_type in ActionIdTypes]
        for field in fields:
            if field in user_action:
                return user_action[:len(field)]

        assert False, "invalid action type!!"
