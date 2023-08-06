from datetime import datetime

from pydantic import BaseModel


class Project(BaseModel):
    id: str
    name: str
    description: str
    is_private: bool
    is_starred: bool
    is_archived: bool
    is_member: bool
    host_id: str
    created: datetime
