from pydantic import BaseModel

from src.ui.button import Button


class ContextMenuItem(BaseModel):
    label: str
    action_id: str


class Header(BaseModel):
    title: str
    subtitle: str | None
    context_menu: list[ContextMenuItem] | None
    buttons: list[Button] | None
