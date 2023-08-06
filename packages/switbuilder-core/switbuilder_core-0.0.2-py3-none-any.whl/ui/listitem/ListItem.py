from pydantic import BaseModel


class ListItem(BaseModel):
    type: str
    action_id: str
    title: str
    subtitle: str
    snippet: str
    draggable: bool = False
