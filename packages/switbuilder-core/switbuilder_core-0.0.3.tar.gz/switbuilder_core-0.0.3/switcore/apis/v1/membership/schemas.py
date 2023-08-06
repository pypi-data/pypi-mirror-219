from datetime import datetime

from pydantic import BaseModel


class Team(BaseModel):
    team_id: str
    team_name: str
    main_dept_yn: str
    created: str


class OrganizationUser(BaseModel):
    user_id: str
    user_name: str
    email: str
    role: int
    status: str
    mode: str
    created: datetime
    tel: str
    timezone: str
    timezone_auto_flag: int
    msg: str
    team: list[Team]
    bg_color: str
    photo: str
    me: bool
    last_activity: datetime
    is_active: bool
    language: str
