from fastapi import HTTPException


class SwitUserNotFoundException(HTTPException):
    def __init__(self, detail: str, swit_request):
        from action.schemas import SwitRequest
        super().__init__(status_code=403, detail=detail)
        self.swit_request: SwitRequest = swit_request


class SwitNeedScopeException(HTTPException):
    def __init__(self, detail: str, swit_request):
        from action.schemas import SwitRequest
        super().__init__(status_code=403, detail=detail)
        self.swit_request: SwitRequest = swit_request
