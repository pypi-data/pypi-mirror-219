from fastapi import APIRouter, Depends, Query
from fastapi import Request
from fastapi.responses import StreamingResponse
from io import BytesIO
from sqlalchemy.orm import Session
from urllib.parse import quote

from action.activity_handler import ActivityHandler
from action.dependencies import get_activity_handler
from auth import service as auth_service
from auth.schemas import UserSchema
from database import get_db_session
from imap import service as imap_service
from ui.swit_response.SwitResponse import SwitResponse

router = APIRouter()


@router.post("/")
async def main(
        activity_handler: ActivityHandler = Depends(get_activity_handler)
):
    swit_response: SwitResponse = await activity_handler.on_turn()
    data = swit_response.dict(exclude_none=True)
    return data


# noinspection PyUnusedLocal
@router.get("/attachment")
async def get_attachment(
        request: Request,
        message_id: str = Query(...),
        index: int = 0,
        swit_id: str = Query(...),
        session: Session = Depends(get_db_session)
):
    user = auth_service.get_user(swit_id, session)
    email = await imap_service.get_email_by_user(UserSchema.from_orm(user), message_id)
    attachment = email.attachments[index]
    file_stream = BytesIO(attachment.raw)
    content_type = f"application/octet-stream"
    response = StreamingResponse(
        file_stream,
        media_type=content_type,
        headers={
            "charset": "utf-8",
            "Content-Disposition": f"attachment; filename={quote(attachment.filename)}"
        },
    )

    return response
