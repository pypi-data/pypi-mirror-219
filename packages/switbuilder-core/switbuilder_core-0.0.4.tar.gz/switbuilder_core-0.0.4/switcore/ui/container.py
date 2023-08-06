from pydantic import BaseModel

from switcore.ui.button import Button


class Container(BaseModel):
    type: str = "container"
    elements: list[Button]
