from typing import Optional

from fastapi import Request, Depends
from sqlalchemy.orm import Session
from httpx_oauth.oauth2 import OAuth2
from httpx_oauth.integrations.fastapi import OAuth2AuthorizeCallback

from action.schemas import SwitRequest
from auth.oauth2 import SwitHttpClient, SwitClientAuth
from auth.schemas import UserSchema
from auth.utils import get_swit_openapi_base_url
from auth.exception import SwitUserNotFoundException
from auth import service as auth_service
from database import get_db_session
from config import settings


async def get_user(request: Request, session: Session = Depends(get_db_session)) -> UserSchema:
    res: dict = await request.json()
    swit_request = SwitRequest(**res)
    user = auth_service.get_user(swit_request.user_info.user_id, session=session)
    if user is None:
        raise SwitUserNotFoundException(detail="User not found", swit_request=swit_request)
    return UserSchema.from_orm(user)


async def get_swit_oauth2() -> OAuth2:
    return OAuth2(  # TODO : 매 호출 마다 생성하지 말고 인스턴스로 박아 둘지 고민
        client_id=settings.SWIT_CLIENT_ID,
        client_secret=settings.SWIT_CLIENT_SECRET,
        authorize_endpoint=f"{get_swit_openapi_base_url()}/oauth/authorize",
        access_token_endpoint=f"{get_swit_openapi_base_url()}/oauth/token",
        refresh_token_endpoint=f"{get_swit_openapi_base_url()}/oauth/token",
        name="swit",
        base_scopes=["app:install"]
    )


async def get_swit_oauth2_callback_bot(
        request: Request,
        code: Optional[str] = None,
        code_verifier: Optional[str] = None,
        state: Optional[str] = None,
        error: Optional[str] = None,
        swit_oauth2: OAuth2 = Depends(get_swit_oauth2)
):
    callback = OAuth2AuthorizeCallback(swit_oauth2, redirect_url=settings.BASE_URL + "/auth/callback/bot")

    return await callback(
        request=request,
        code=code,
        code_verifier=code_verifier,
        state=state,
        error=error
    )


async def get_swit_oauth2_callback_user(
        request: Request,
        code: Optional[str] = None,
        code_verifier: Optional[str] = None,
        state: Optional[str] = None,
        error: Optional[str] = None,
        swit_oauth2: OAuth2 = Depends(get_swit_oauth2)
):
    callback = OAuth2AuthorizeCallback(swit_oauth2, redirect_url=settings.BASE_URL + "/auth/callback/user")

    return await callback(
        request=request,
        code=code,
        code_verifier=code_verifier,
        state=state,
        error=error
    )


async def get_swit_oauth2_callback_authorize(
        request: Request,
        code: Optional[str] = None,
        code_verifier: Optional[str] = None,
        state: Optional[str] = None,
        error: Optional[str] = None,
        swit_oauth2: OAuth2 = Depends(get_swit_oauth2)
):
    callback = OAuth2AuthorizeCallback(swit_oauth2, redirect_url=settings.BASE_URL + "/auth/callback/authorize")

    return await callback(
        request=request,
        code=code,
        code_verifier=code_verifier,
        state=state,
        error=error
    )


async def get_swit_http_client(
        request: Request,
        swit_oauth2: OAuth2 = Depends(get_swit_oauth2),
        user: UserSchema = Depends(get_user),
        session: Session = Depends(get_db_session)
) -> SwitHttpClient:
    client = None
    res: dict = await request.json()
    swit_request = SwitRequest(**res)
    try:
        client = SwitHttpClient(
            swit_request=swit_request,
            auth=SwitClientAuth(
                swit_oauth2,
                user.swit_id,
                user.access_token,
                user.refresh_token,
                session
            ),
            timeout=25.0,
            base_url=get_swit_openapi_base_url()
        )
        yield client
    finally:
        if client:
            await client.aclose()
