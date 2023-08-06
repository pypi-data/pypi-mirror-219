import os

from fastapi import Request, Depends
from fastapi.security import OAuth2

from switcore.auth.utils import get_swit_openapi_base_url


async def get_swit_oauth2() -> OAuth2:
    print(os.getenv('SWIT_CLIENT_ID'))
    return OAuth2(
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
        code: str | None = None,
        code_verifier: str | None = None,
        state: str | None = None,
        error: str | None = None,
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
