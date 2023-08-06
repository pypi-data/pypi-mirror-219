from fastapi import HTTPException

from auth.schemas import UserSchema
from exception import LoggingException


class ImapLoginFailedException(HTTPException):

    def __init__(self, detail: str, swit_id: str, email: str, password: str, url: str, use_tls: bool):
        super().__init__(status_code=401, detail=detail)
        self.swit_id = swit_id
        self.email = email
        self.password = password
        self.url = url
        self.use_tls = use_tls


class ImapDisconnectFailedException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)


class EmailFetchFailedException(LoggingException):
    def __init__(self, detail: str, user: UserSchema):
        super().__init__(status_code=500, detail=detail)
        self.user = user


class InvalidConnectionException(LoggingException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail)


class CannotReadException(LoggingException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail)
