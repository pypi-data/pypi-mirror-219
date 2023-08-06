import os

from typing import Literal, Optional

from starlette.requests import HTTPConnection
from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from itsdangerous import Signer

from .backend.base import BaseAsyncBackend
from .ext.encoding import JsonEncoding, BaseEncoding


class SessionMiddleware:
    def __init__(
            self,
            app: ASGIApp,
            backend: BaseAsyncBackend,
            secret_key: str,
            prefix_cookie: str = "s",
            max_age: Optional[int] = 604800,  # 7 days, in seconds
            path: str = "/",
            same_site: Literal["lax", "strict", "none"] = "lax",
            https_only: bool = False,
            encoder: BaseEncoding = JsonEncoding
    ) -> None:
        self.app = app
        self.backend = backend
        self.session_cookie = prefix_cookie
        self.max_age = max_age
        self.path = path
        self.security_flags = "httponly; samesite=" + same_site

        if https_only:  # Secure flag can be used with HTTPS only
            self.security_flags += "; secure"

        self.encoder = encoder
        self.signer = Signer(secret_key)

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        connection = HTTPConnection(scope)

        initial_session_was_empty = True
        session_id = None

        # session exists or not
        if self.session_cookie in connection.cookies:
            # get data session by session_id
            signer_session_id = connection.cookies[self.session_cookie].encode("utf-8")

            if self.signer.validate(signer_session_id):
                session_id = signer_session_id.decode().split('.')[0]
                data_session = await self.backend.get(session_id)

                if data_session:
                    scope["session"] = self.encoder.loads(data_session)
                    initial_session_was_empty = False

        if initial_session_was_empty:
            scope["session"] = {}

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                cookies = None

                if scope["session"]:
                    if initial_session_was_empty:
                        # new session
                        new_session_id = os.urandom(32).hex()
                        signer_session = self.signer.sign(new_session_id).decode()
                        await self.backend.set(new_session_id, self.encoder.dumps(scope["session"]), self.max_age)

                        cookies = self._create_cookie(signer_session)
                    else:
                        # update session
                        await self.backend.update(session_id, self.encoder.dumps(scope["session"]))
                else:
                    if not initial_session_was_empty:
                        # server delete session
                        await self.backend.delete(session_id)
                    cookies = self._create_cookie(clear=True)

                if cookies:
                    headers.append("Set-Cookie", cookies)

            await send(message)

        await self.app(scope, receive, send_wrapper)

    def _create_cookie(self, data: Optional[str] = None, clear: bool = False) -> str:
        if not clear:
            return f"{self.session_cookie}={data}; path={self.path}; {self.max_age}{self.security_flags}"
        else:
            return f"{self.session_cookie}=null; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; {self.security_flags}"
