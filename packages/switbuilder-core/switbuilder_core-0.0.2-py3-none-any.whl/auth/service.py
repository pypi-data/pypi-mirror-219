from typing import Final, Optional
from urllib import parse

import jwt
from sqlalchemy.orm import Session

from auth import exception
from auth.models import User
from auth.repository import AppRepository, UserRepository
from auth.schemas import SwitToken, Payload, UserSchema
from auth.utils import get_swit_openapi_base_url
from config import settings
from imap import service as imap_service


def get_oauth2_url(
    scopes: str,
    redirect_url: str
) -> str:
    params: Final[dict] = {
        "client_id": settings.SWIT_CLIENT_ID,
        "redirect_uri": settings.BASE_URL + redirect_url,
        "response_type": "code",
        "scope": scopes
    }

    return f"{get_swit_openapi_base_url()}/oauth/authorize?{parse.urlencode(params)}"


async def save_swit_app(
    session: Session,
    token: SwitToken,
    state: Optional[str] = None
):
    repository = AppRepository(session)

    # if not res.is_success:
    #     raise exception.AuthorizationException("invalid auth code!")

    payload = Payload(**jwt.decode(token.access_token, options={"verify_signature": False}))
    return repository.create(
        access_token=token.access_token,
        refresh_token=token.refresh_token,
        apps_id=payload.apps_id,
        cmp_id=payload.cmp_id,
        iss=payload.iss
    )


async def save_swit_user(
    session: Session,
    token: SwitToken,
    state: Optional[str] = None,
) -> User:
    user_repository = UserRepository(session)

    # if not res.is_success:
    #     raise exception.AuthorizationException("invalid auth code!")

    payload = Payload(**jwt.decode(token.access_token, options={"verify_signature": False}))

    # user token 에서 payload.sub 는 user_id
    # bot token 에서 sub 는 cmp_id(org_id)
    swit_id = payload.sub
    return user_repository.get_or_create(
        swit_id=swit_id,
        access_token=token.access_token,
        refresh_token=token.refresh_token,
    )


def get_user(swit_id: str, session: Session) -> User | None:
    repository = UserRepository(session)
    return repository.get_by_swit_id(swit_id)


async def delete(user: UserSchema, session: Session) -> None:
    await imap_service.disconnect(user)
    repository = UserRepository(session)
    repository.delete(user.swit_id)
