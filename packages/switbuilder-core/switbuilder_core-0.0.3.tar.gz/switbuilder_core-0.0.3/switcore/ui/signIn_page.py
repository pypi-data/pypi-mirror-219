from pydantic import BaseModel

from src.ui.button import Button
from src.ui.Icon import Icon


class IntegratedService(BaseModel):
    icon: Icon


class SignInPage(BaseModel):
    id: str | None = None
    type: str = "sign_in_page"
    integrated_service: IntegratedService
    title: str
    description: str
    button: Button
