from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List

import httpx
from fastapi import Request
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session

from action.constants import init_state, PlatformTypes
from action.exceptions import InvalidStateException
from auth.oauth2 import SwitHttpClient
from auth.schemas import UserSchema
from ui.swit_response.AttachmentView import AttachmentView
from ui.swit_response.View import View
from ui.utils import compress_and_b64encode, b64decode_and_decompress
from workspace.schemas import Workspace


class UserInfo(BaseModel):
    user_id: str
    organization_id: str


class UserPreferences(BaseModel):
    language: str
    time_zone_offset: str
    color_theme: str


class Resource(BaseModel):
    resource_type: str
    id: str
    created_at: datetime
    edited_at: datetime
    content: str
    content_formatted: Dict[str, Any]
    attachments: Optional[List[Dict[str, Any]]]
    files: Optional[List[Dict[str, Any]]]
    creator: Dict[str, Any]


class UserActionType(str, Enum):
    right_panel_open = "right_panel_open"
    presence_sync = "presence_sync"
    user_commands_chat = "user_commands.extensions:chat"
    user_commands_chat_extension = "user_commands.chat_extension"
    user_commands_chat_commenting = "user_commands.extensions:chat_commenting"
    user_commands_context_menus_message = "user_commands.context_menus:message"
    user_commands_context_menus_message_comment = "user_commands.context_menus:message_comment"
    view_actions_drop = "view_actions.drop"
    view_actions_input = "view_actions.input"
    view_actions_submit = "view_actions.submit"
    view_actions_oauth_complete = "view_actions.oauth_complete"


class UserAction(BaseModel):
    type: UserActionType
    id: str
    slash_command: str
    resource: Resource | None
    value: str | None = None


class Context(BaseModel):
    workspace_id: str
    channel_id: str


class SwitRequest(BaseModel):
    platform: PlatformTypes
    time: datetime
    app_id: str
    user_info: UserInfo
    user_preferences: UserPreferences
    context: Context
    user_action: UserAction
    current_view: View | AttachmentView | None

    @validator('current_view', pre=True)
    def empty_dict_to_null(cls, v):
        if v == {}:
            return None
        return v


class ActionRequest(SwitRequest):
    origin_reqeust: Request
    user: UserSchema
    session: Session
    swit_client: SwitHttpClient

    class Config:
        arbitrary_types_allowed = True


class State(BaseModel):
    label: str
    seq: int
    limit: int
    scope: str = "ALL"
    keyword: str | None
    search_type: str = "LATEST"
    email_list_view: dict = {}  # 뒤로 가기 읽음 처리를 위함
    email_action_id: str = ""  # 뒤로 가기 읽음 처리를 위함
    shared_email_id: str = ""  # 공유 하기
    workspace_id: str = ""
    channel_id: str = ""
    workspaces: list[Workspace] = []  # 공유 모달 select
    channels: list[Workspace] = []  # 공유 모달 select
    email_detail_raw: str = ''  # task 변환 시 사용
    email_detail_message_id: str = ''  # task 변환 시 사용
    prev_view: dict = {}  # Need Scope Modal 뒤로 가기 시 사용

    @staticmethod
    def from_bytes(byte: bytes) -> 'State':
        d = b64decode_and_decompress(byte)
        return State(**d)

    # noinspection PyMethodMayBeStatic
    def is_valid(self, state: dict | None = None, raise_exception: bool = True) -> bool:
        if state is None:
            state = init_state

        for key in state:
            has_key = init_state.get(key, None)
            if has_key is None:
                if raise_exception:
                    raise InvalidStateException(detail=f'state must have {key} key!!')

                return False

        return True

    def update(self, new_state: dict) -> 'State':
        seq: int | None = new_state.get('seq', None)
        if seq and seq <= 0:
            new_state['seq'] = init_state['seq']

        if self.is_valid(new_state):
            return State(**{**self.dict(), **new_state})

    def to_bytes(self) -> bytes:
        return compress_and_b64encode(self.dict())

    def refresh(self) -> 'State':
        return self.update(
            {
                "label": init_state["label"],
                "seq": init_state["seq"],
                "limit": init_state["limit"],
                "keyword": init_state["keyword"],
                "email_detail_raw": init_state["email_detail_raw"],
            }
        )
