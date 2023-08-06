import typing

import httpx
from httpx import AsyncClient, Response, AsyncBaseTransport, Limits
from httpx._client import UseClientDefault, USE_CLIENT_DEFAULT
from httpx._config import DEFAULT_TIMEOUT_CONFIG, DEFAULT_LIMITS, DEFAULT_MAX_REDIRECTS
from httpx._types import URLTypes, RequestContent, RequestData, RequestFiles, QueryParamTypes, HeaderTypes, CookieTypes, \
    AuthTypes, TimeoutTypes, RequestExtensions, VerifyTypes, CertTypes, ProxiesTypes
from httpx_oauth.oauth2 import OAuth2, OAuth2Token, RefreshTokenError
from sqlalchemy.orm import Session

from auth.constants import ErrorCode
from auth.exception import SwitNeedScopeException
from auth.repository import UserRepository
from logger import get_logger


class SwitHttpClient(AsyncClient):

    def __init__(self, *, swit_request, auth: typing.Optional[AuthTypes] = None,
                 params: typing.Optional[QueryParamTypes] = None,
                 headers: typing.Optional[HeaderTypes] = None, cookies: typing.Optional[CookieTypes] = None,
                 verify: VerifyTypes = True, cert: typing.Optional[CertTypes] = None, http1: bool = True,
                 http2: bool = False, proxies: typing.Optional[ProxiesTypes] = None,
                 mounts: typing.Optional[typing.Mapping[str, AsyncBaseTransport]] = None,
                 timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG, follow_redirects: bool = False,
                 limits: Limits = DEFAULT_LIMITS, max_redirects: int = DEFAULT_MAX_REDIRECTS,
                 event_hooks: typing.Optional[
                     typing.Mapping[str, typing.List[typing.Callable[..., typing.Any]]]
                 ] = None, base_url: URLTypes = "", transport: typing.Optional[AsyncBaseTransport] = None,
                 app: typing.Optional[typing.Callable[..., typing.Any]] = None, trust_env: bool = True,
                 default_encoding: typing.Union[str, typing.Callable[[bytes], str]] = "utf-8"):
        from action.schemas import SwitRequest

        self.swit_request: SwitRequest = swit_request
        super().__init__(auth=auth, params=params, headers=headers, cookies=cookies, verify=verify, cert=cert,
                         http1=http1, http2=http2, proxies=proxies, mounts=mounts, timeout=timeout,
                         follow_redirects=follow_redirects, limits=limits, max_redirects=max_redirects,
                         event_hooks=event_hooks, base_url=base_url, transport=transport, app=app, trust_env=trust_env,
                         default_encoding=default_encoding)

    async def request(self, method: str, url: URLTypes, *, content: typing.Optional[RequestContent] = None,
                      data: typing.Optional[RequestData] = None, files: typing.Optional[RequestFiles] = None,
                      json: typing.Optional[typing.Any] = None, params: typing.Optional[QueryParamTypes] = None,
                      headers: typing.Optional[HeaderTypes] = None, cookies: typing.Optional[CookieTypes] = None,
                      auth: typing.Union[AuthTypes, UseClientDefault, None] = USE_CLIENT_DEFAULT,
                      follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
                      timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
                      extensions: typing.Optional[RequestExtensions] = None) -> Response:

        request = self.build_request(
            method=method,
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

        response: Response = await self.send(request, auth=auth, follow_redirects=follow_redirects)
        if response.status_code == 403:
            data: dict = response.json()
            error_or_null: dict | None = data.get('error', None)
            if error_or_null:
                code_or_null: int | None = error_or_null.get('code', None)
                if code_or_null and code_or_null == ErrorCode.NEED_SCOPE:
                    raise SwitNeedScopeException(detail="need scope", swit_request=self.swit_request)
        return response


class SwitClientAuth(httpx.Auth):
    requires_response_body = True

    def __init__(
            self,
            swit_oauth2: OAuth2,
            swit_id: str,
            access_token: str,
            refresh_token: str,
            session: Session
    ):
        self.swit_oauth2 = swit_oauth2
        self.swit_id = swit_id
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.session = session

    async def async_auth_flow(self, request):
        # Auth 가 탑재된 AsyncClient 에서 request 를 보낼 때 먼저 실행 됨
        request.headers["Authorization"] = f"Bearer {self.access_token}"
        response = yield request
        if response.status_code == 401:
            # If the server issues a 401 response, then issue a request to
            # refresh tokens, and resend the request.
            try:
                new_token = await self.swit_oauth2.refresh_token(self.refresh_token)
                self.update_tokens(new_token)
            except RefreshTokenError as exc:
                logger = get_logger("async_auth_flow")
                logger.error(f"can not refresh token!!: {str(exc)}")
                UserRepository(self.session).delete(self.swit_id)

            request.headers["Authorization"] = f"Bearer {self.access_token}"
            yield request

    def update_tokens(self, new_token: OAuth2Token):
        self.access_token = new_token["access_token"]
        self.refresh_token = new_token["refresh_token"]
        # session 으로 디비 변경
        UserRepository(self.session).update(
            self.swit_id, self.access_token, self.refresh_token)
