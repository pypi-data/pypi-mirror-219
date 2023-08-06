import base64
import logging

from action.schemas import ActionRequest
from emails.utils import get_share_to_dm_url
from imap.utils import decode_to_bytes_from_base64
from logger import logger_decorator


@logger_decorator()
async def share_to_dm(
        action_request: ActionRequest,
        mail_raw: str,
        room_or_user_id: str,
        logger: logging.Logger
):
    data = {
        "provider": "gmail",  # TODO imap provider
        "mail": base64.urlsafe_b64encode(decode_to_bytes_from_base64(mail_raw)).decode(),
        "target_id": room_or_user_id,
    }

    res = await action_request.swit_client.post(get_share_to_dm_url(), json=data)
    if res.status_code != 200:
        logger.error(f"convert_to_new_task error: {res.json()}")
