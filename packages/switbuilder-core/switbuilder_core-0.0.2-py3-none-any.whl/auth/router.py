import jwt
from fastapi import APIRouter, Depends, status, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from httpx_oauth.oauth2 import OAuth2
from sqlalchemy.orm import Session

from auth import dependencies
from auth import service as auth_service
from auth.repository import UserRepository
from auth.schemas import UserSchema, SwitToken, Payload
from config import settings
from database import get_db_session
from imap import service as imap_service
from jinja import templates
from lokalise import get_translated_text

router = APIRouter()


@router.get("/bot", name="auth_bot")
async def bot_install_oauth2(
        request: Request,
        swit_oauth2: OAuth2 = Depends(dependencies.get_swit_oauth2)
):
    return RedirectResponse(
        await swit_oauth2.get_authorization_url(
            redirect_uri=settings.BASE_URL + "/auth/callback/bot",
            scope=["app:install"]
        ),
        status.HTTP_307_TEMPORARY_REDIRECT
    )


@router.get("/user", name="auth_user")
async def user_oauth2(
        request: Request,
        swit_oauth2: OAuth2 = Depends(dependencies.get_swit_oauth2)
):
    return RedirectResponse(
        await swit_oauth2.get_authorization_url(
            redirect_uri=settings.BASE_URL + "/auth/callback/user",
            scope=[
                # "imap:write+imap:read+user:read+message:write+channel:read+workspace:read+project:read+project:write+task:read+task:write"]
            "imap:write+imap:read+user:read+message:write+channel:read+workspace:read"]
            # "imap:write+imap:read+user:read"]
            # TODO 무조건 변경!
        ),
        status.HTTP_307_TEMPORARY_REDIRECT
    )


@router.get("/authorize", name="auth_authorize")
async def user_oauth2(
        request: Request,
        swit_oauth2: OAuth2 = Depends(dependencies.get_swit_oauth2)
):
    return RedirectResponse(
        await swit_oauth2.get_authorization_url(
            redirect_uri=settings.BASE_URL + "/auth/callback/authorize",
            scope=[
                "imap:write+imap:read+user:read+message:write+channel:read+workspace:read+project:read+project:write+task:read+task:write"]
        ),
        status.HTTP_307_TEMPORARY_REDIRECT
    )


@router.get("/callback/bot", name="auth_callback_bot")
async def bot_install_callback(
        token_state=Depends(dependencies.get_swit_oauth2_callback_bot),
        session=Depends(get_db_session)
):
    token, state = token_state
    await auth_service.save_swit_app(session, SwitToken(**token), state)
    return HTMLResponse(content="<script>window.close()</script>")


@router.get("/callback/user", name="auth_callback_user")
async def user_login_callback(
        request: Request,
        token_state=Depends(dependencies.get_swit_oauth2_callback_user),
        session=Depends(get_db_session)
):
    token, state = token_state
    user = await auth_service.save_swit_user(session, SwitToken(**token), state)
    email_account_message = get_translated_text("ko", "ifyouremailaccounthas2tep")

    email: str = ''
    password: str = ''
    url: str = ''
    use_tls: bool = True

    return templates.TemplateResponse(
        "imap_signin.html",
        {
            "request": request,
            "swit_id": user.swit_id,
            "base_url": settings.BASE_URL,
            "is_valid": True,
            "email_account_message": email_account_message,
            "emails": email,
            "password": password,
            "url": url,
            "use_tls": use_tls
        }
    )


@router.get("/callback/authorize", name="authorize_callback")
async def authorize_callback(
        request: Request,
        token_state=Depends(dependencies.get_swit_oauth2_callback_authorize),
        session=Depends(get_db_session)
):
    token, state = token_state
    access_token: str = token.get('access_token', None)
    refresh_token: str = token.get('refresh_token', None)

    assert access_token is not None, "access_token is None"
    assert refresh_token is not None, "refresh_token is None"

    payload = Payload(**jwt.decode(access_token, options={"verify_signature": False}))
    swit_id = payload.sub
    user_repository = UserRepository(session)
    user_repository.update(swit_id, access_token, refresh_token)

    return templates.TemplateResponse(
        "close_after_oauth.html",
        {
            "request": request,
        }
    )


@router.post("/example")
async def post_example(
        request: Request,
        swit_id: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        url: str = Form(...),
        use_tls: bool = Form(False),
        session: Session = Depends(get_db_session)
):
    user = auth_service.get_user(swit_id, session)

    await imap_service.connect(
        user=UserSchema.from_orm(user),
        email=email,
        password=password,
        url=url,
        use_tls=use_tls
    )

    return templates.TemplateResponse(
        "close_after_oauth.html",
        {
            "request": request,
        }
    )
