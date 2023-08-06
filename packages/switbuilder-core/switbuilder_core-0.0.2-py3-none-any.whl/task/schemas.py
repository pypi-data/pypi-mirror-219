from typing import List, Optional
from pydantic import BaseModel


class TaskAsset(BaseModel):
    file_desc: str
    file_mime: str
    file_name: str
    file_path: str
    file_size: int
    thumbnail: str


class TaskStatusCustom(BaseModel):
    color_label: str
    status_attribute: str
    status_id: str
    status_name: str


class Task(BaseModel):
    assets: List[TaskAsset] = []
    assign: str
    assignees: List[str]
    bucket_id: str
    color: str
    comment_count: int
    content: str
    end_date: str
    follow: List[str]
    id: str
    isTime: bool
    priority: str
    project_id: str
    rich_text: bool
    start_date: str
    status: str
    status_custom: TaskStatusCustom
    title: str
    user_id: str
    parent_id: Optional[str]
    subtask_count: str
