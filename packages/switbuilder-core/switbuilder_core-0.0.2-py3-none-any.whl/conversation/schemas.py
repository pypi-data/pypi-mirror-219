from datetime import datetime

from pydantic import BaseModel


class Room(BaseModel):
    room_id: str
    room_type: str
    created: datetime
    is_starred: bool
    unread_count: int
    member_count: int
    members: list[str]
    room_name: str
    direct_user_id: str
    last_read: datetime
    is_hidden: bool
    push_type: str
    contents: dict | None
    status: str

    @property
    def room_or_user_id(self):
        if self.room_type == "direct message":
            return self.direct_user_id
        else:
            return self.room_id
