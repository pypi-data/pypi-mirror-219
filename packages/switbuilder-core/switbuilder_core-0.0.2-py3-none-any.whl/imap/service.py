import base64
import logging
from typing import Final, Optional

import httpx
from httpx import ReadTimeout
from starlette import status

from action.schemas import ActionRequest, State
from auth.schemas import UserSchema
from auth.utils import get_swit_openapi_base_url
from config import settings
from imap.exception import ImapLoginFailedException, ImapDisconnectFailedException, EmailFetchFailedException, \
    InvalidConnectionException, CannotReadException
from imap.schemas import EmailList, EmailDetail
from imap.utils import get_mails_url, get_mail_url, get_connect_url, get_disconnect_url, get_share_url, \
    decode_to_bytes_from_base64, get_labels_url, get_read_url
from logger import logger_decorator


@logger_decorator()
async def connect(
        user: UserSchema,
        email: str,
        password: str,
        url: str,
        logger: Optional[logging.Logger] = None,
        use_tls: bool = True
):
    # TODO : 이 함수는 auth 에서 호출하고 있는데 이 방향이 어색해 보임.
    #        api 호출을 auth 가 아닌 다른 곳으로 받고 user_action 로직처럼 swit_client 를 만들어서 처리 필요
    header: Final[dict] = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {user.access_token}",
    }

    data: Final[dict] = {
        "apps_id": settings.APPS_ID,
        "email": email,
        "host": url,
        "is_tls": use_tls,
        "password": password,
        "port": "993" if use_tls else "143"
    }

    try:
        await disconnect(user)
    except ImapDisconnectFailedException as e:
        logger.error(f"ImapDisconnectFailedException: {str(e)}")

    async with httpx.AsyncClient() as client:
        res = await client.post(get_connect_url(), headers=header, json=data)

    if not res.is_success:
        logger.error(res.json())
        raise ImapLoginFailedException(
            detail="User not found", swit_id=user.swit_id, email=email, password=password, url=url, use_tls=use_tls)


async def disconnect(user: UserSchema):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {user.access_token}",
    }

    data = {
        "apps_id": settings.APPS_ID
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(get_disconnect_url(), headers=headers, json=data)

    if not res.is_success:
        raise ImapDisconnectFailedException(detail="unable to logout !!")


@logger_decorator()
async def get_mails(
        action_request: ActionRequest,
        new_state: State,
        logger: Optional[logging.Logger] = None
) -> list[EmailList]:
    params: dict = {
        "apps_id": settings.APPS_ID,
        "label": new_state.label,
        "seq": new_state.seq,
        "limit": new_state.limit,
        "scope": "ALL",
        "search_type": "LATEST",
    }

    if new_state.keyword:
        params["keyword"] = new_state.keyword

    try:
        res = await action_request.swit_client.get(
            get_mails_url(),
            params=params,
        )
    except ReadTimeout as e:
        request = e.request
        logger.error(f"Timeout when making request: {request.method} {request.url} {request.headers}")
        raise EmailFetchFailedException(detail="can not get emails list!! ", user=action_request.user)
    if res.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise InvalidConnectionException(detail=res.json())

    if not res.is_success:
        raise EmailFetchFailedException(detail=res.json(), user=action_request.user)

    mails = res.json()
    if not mails['data']:
        return []

    email_lists: list[EmailList] = [EmailList(**data) for data in mails['data']['mails']]
    return email_lists


async def get_mail(
        action_request: ActionRequest,
        message_id: str
) -> EmailDetail:
    params: Final[dict] = {
        "apps_id": settings.APPS_ID,
        "label": "INBOX",
        "message_id": message_id,
    }

    res = await action_request.swit_client.get(get_mail_url(), params=params)

    mail = res.json()
    # TODO 없으면 예외처리
    email_detail = EmailDetail(**mail['data']['mail_detail'])
    return email_detail


async def get_email_by_user(
        user: UserSchema,
        message_id: str
) -> EmailDetail:
    header: Final[dict] = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {user.access_token}",
    }

    params: Final[dict] = {
        "apps_id": settings.APPS_ID,
        "label": "INBOX",
        "message_id": message_id,
    }
    # TODO : 여기는 첨부파일 부분이라 client 적용 어떻게 할지 논의 필요
    async with httpx.AsyncClient(timeout=20) as client:
        res = await client.get(f'{get_swit_openapi_base_url()}/{get_mail_url()}', headers=header, params=params)

    mail = res.json()
    email_detail = EmailDetail(**mail['data']['mail_detail'])
    return email_detail


@logger_decorator()
async def get_labels(
        action_request: ActionRequest,
        logger: logging.Logger
        # logger_or_null: logging.Logger | None = None
) -> list[str]:
    # logger_or_null
    params: Final[dict] = {
        "apps_id": settings.APPS_ID,
    }

    res = await action_request.swit_client.get(
        get_labels_url(),
        params=params,
        timeout=20
    )

    labels = ["INBOX"]

    new_labels_data: dict = res.json()
    new_labels_or_null = new_labels_data.get('data', None)
    if not new_labels_or_null:
        return labels

    return [label['name'] for label in new_labels_data['data']['labels']]


@logger_decorator()
async def read(
        action_request: ActionRequest,
        message_id: str, label: str, logger: Optional[logging.Logger] = None
):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {action_request.user.access_token}",
    }

    data = {
        "apps_id": settings.APPS_ID,
        "label": label,
        "message_id": message_id
    }

    async with httpx.AsyncClient() as client:  # TODO client 변경
        res = await client.post(get_read_url(), headers=headers, json=data)

    if not res.is_success:
        raise CannotReadException(detail=f"emails cannot read {message_id}")


async def share_to_channel(
        action_request: ActionRequest,
        email: EmailDetail,
        workspace_id: str,
        channel_id: str
):
    data: Final[dict] = {
        "workspace_id": workspace_id,
        "channel_id": channel_id,
        "content": "Shared emails",
        "mail": base64.urlsafe_b64encode(decode_to_bytes_from_base64(email.raw)).decode(),
        "provider": "imap",
    }

    res = await action_request.swit_client.post(get_share_url(), json=data)
