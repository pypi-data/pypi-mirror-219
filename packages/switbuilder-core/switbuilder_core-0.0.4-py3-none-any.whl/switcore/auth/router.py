from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2

from switcore.auth import dependencies

router = APIRouter()


@router.get("/bot", name="auth_bot")
async def bot_install_oauth2(
        request: Request,  # noqa: F841
        swit_oauth2: OAuth2 = Depends(dependencies.get_swit_oauth2)
):
    return RedirectResponse(
        await swit_oauth2.get_authorization_url(
            redirect_uri=settings.BASE_URL + "/auth/callback/bot",
            scope=["app:install"]
        ),
        status.HTTP_307_TEMPORARY_REDIRECT
    )


@router.get("/callback/bot", name="auth_callback_bot")
async def bot_install_callback(
        token_state=Depends(dependencies.get_swit_oauth2_callback_bot),
        session=Depends(get_db_session)
):
    token, state = token_state
    await auth_service.save_swit_app(session, SwitToken(**token))
    return HTMLResponse(content="<script>window.close()</script>")
