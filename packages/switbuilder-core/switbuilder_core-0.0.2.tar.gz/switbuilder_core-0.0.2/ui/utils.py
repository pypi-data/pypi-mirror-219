import base64
import bz2
import json

from action.constants import ActionIdTypes
from imap.constants import invalid_labels


def compress_and_b64encode(data: dict) -> bytes:
    """ 압축 후 base64 인코딩해서 줌 """
    return base64.b64encode(bz2.compress(json.dumps(data).encode("utf-8"), 1))


def b64decode_and_decompress(compressed_data: bytes) -> dict:
    """ base64 디코딩 후 압축 해제해서 줌 """
    return json.loads(bz2.decompress(base64.b64decode(compressed_data)).decode("utf-8"))


def add_action_id(action_type: ActionIdTypes, data: str = '') -> str:
    return f'{action_type.value}::{data}'


def get_attachment_query_param(message_id: str, index: int, swit_id: str) -> str:
    return f"message_id={message_id}&index={index}&swit_id={swit_id}"


def exclude_invalid_labels(labels: list[str]) -> list[str]:
    ret = []
    for label in labels:
        if label in invalid_labels:
            continue
        ret.append(label)
    return ret

