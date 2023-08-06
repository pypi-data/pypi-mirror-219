from pydantic import BaseModel

from ui.common.Button import Button


class Container(BaseModel):
    type: str = "container"
    elements: list[Button]
