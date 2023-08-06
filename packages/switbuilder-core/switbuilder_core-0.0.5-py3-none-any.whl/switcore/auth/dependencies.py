import os

from fastapi import Request, Depends
from httpx_oauth.integrations.fastapi import OAuth2AuthorizeCallback
from httpx_oauth.oauth2 import OAuth2

from switcore.auth.utils import get_swit_openapi_base_url


async def get_swit_oauth2() -> OAuth2:
    swit_client_id: str = os.getenv('SWIT_CLIENT_ID', None)
    swit_client_secret: str = os.getenv('SWIT_CLIENT_SECRET', None)

    assert swit_client_id is not None, "SWIT_CLIENT_ID is not set check .env file"
    assert swit_client_secret is not None, "SWIT_CLIENT_SECRET is not set check .env file"

    return OAuth2(
        client_id=swit_client_id,
        client_secret=swit_client_secret,
        authorize_endpoint=f"{get_swit_openapi_base_url()}/oauth/authorize",
        access_token_endpoint=f"{get_swit_openapi_base_url()}/oauth/token",
        refresh_token_endpoint=f"{get_swit_openapi_base_url()}/oauth/token",
        name="swit",
        base_scopes=["app:install"]
    )


async def get_swit_oauth2_callback_bot(
        request: Request,
        code: str | None = None,
        code_verifier: str | None = None,
        state: str | None = None,
        error: str | None = None,
        swit_oauth2: OAuth2 = Depends(get_swit_oauth2)
):
    base_url: str = os.getenv('BASE_URL', None)
    assert base_url is not None, "BASE_URL is not set check .env file"
    callback = OAuth2AuthorizeCallback(swit_oauth2, redirect_url=base_url + "/auth/callback/bot")

    return await callback(
        request=request,
        code=code,
        code_verifier=code_verifier,
        state=state,
        error=error
    )
