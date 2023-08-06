from pydantic import BaseModel

from src.ui.select_item import SelectItem


class Tabs(BaseModel):
    """
        An element representing an array of tabs.
    """
    type = "tabs"
    tabs: list[SelectItem]
    value: str
