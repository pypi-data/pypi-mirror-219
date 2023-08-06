# from typing import Final, Optional
# from urllib import parse
#
# import jwt
# from sqlalchemy.orm import Session
#
#
#
# def get_oauth2_url(
#     scopes: str,
#     redirect_url: str
# ) -> str:
#     params: Final[dict] = {
#         "client_id": settings.SWIT_CLIENT_ID,
#         "redirect_uri": settings.BASE_URL + redirect_url,
#         "response_type": "code",
#         "scope": scopes
#     }
#
#     return f"{get_swit_openapi_base_url()}/oauth/authorize?{parse.urlencode(params)}"
#
#
# async def save_swit_app(
#     session: Session,
#     token: SwitToken
# ):
#     repository = AppRepository(session)
#     payload = Payload(**jwt.decode(token.access_token, options={"verify_signature": False}))
#     return repository.create(
#         access_token=token.access_token,
#         refresh_token=token.refresh_token,
#         apps_id=payload.apps_id,
#         cmp_id=payload.cmp_id,
#         iss=payload.iss
#     )
#
#
