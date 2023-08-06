from pydantic import BaseModel

from src.ui.button import Button


class Container(BaseModel):
    type: str = "container"
    elements: list[Button]
