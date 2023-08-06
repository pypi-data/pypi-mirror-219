from pydantic import BaseModel
from enum import Enum

from switcore.ui.static_action import StaticAction


class FileType(str, Enum):
    image = "image"
    video = "video"
    document = "document"
    pdf = "pdf"
    presentation = "presentation"
    spreadsheet = "spreadsheet"
    archive = "archive"
    psd = "psd"
    ai = "ai"
    other = "other"


def get_file_type(file_extension: str) -> FileType:
    if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
        file_type = FileType.image
    elif file_extension in ['mp4', 'avi', 'mov']:
        file_type = FileType.video
    elif file_extension in ['doc', 'docx', 'txt']:
        file_type = FileType.document
    elif file_extension == 'pdf':
        file_type = FileType.pdf
    elif file_extension in ['ppt', 'pptx']:
        file_type = FileType.presentation
    elif file_extension == 'xls':
        file_type = FileType.spreadsheet
    elif file_extension in ['zip', 'rar']:
        file_type = FileType.archive
    elif file_extension == 'psd':
        file_type = FileType.psd
    elif file_extension == 'ai':
        file_type = FileType.ai
    else:
        file_type = FileType.other

    return file_type


class File(BaseModel):
    type: str = "file"
    file_type: FileType
    file_size: int
    file_name: str
    action_id: str | None
    static_action: StaticAction | None
