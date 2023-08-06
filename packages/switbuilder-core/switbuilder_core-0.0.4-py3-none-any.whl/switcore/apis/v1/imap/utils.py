import base64
import datetime
import re
from email.header import decode_header
from email.message import Message

from babel.dates import format_time, format_date
from bs4 import BeautifulSoup

from action.constants import PlatformTypes
from action.schemas import UserPreferences
from config import settings
from auth.utils import get_swit_openapi_base_url


def decode_to_bytes_from_base64(encoded: str) -> bytes:
    return base64.urlsafe_b64decode(encoded)


def decode_to_str_from_base64(encoded: str) -> str:
    return base64.urlsafe_b64decode(encoded).decode()


def get_mails_url() -> str:
    return 'v1/api/imap.mails'


def get_labels_url() -> str:
    return 'v1/api/imap.labels'


def get_mail_url() -> str:
    return 'v1/api/imap.mail'


def get_connect_url() -> str:
    return f'{get_swit_openapi_base_url()}/v1/api/imap.connection'


def get_disconnect_url() -> str:
    return f'{get_swit_openapi_base_url()}/v1/api/imap.connection.delete'


def get_read_url() -> str:
    return f'{get_swit_openapi_base_url()}/v1/api/imap.mail.read'


# def get_read_url() -> str:
#     return f'v1/api/imap.mail.read'


def get_share_url() -> str:
    return 'v1/api/message.mail.create'


def create_html_content(text: str) -> str:
    newline_chars = ["\r\n", "\n", "\r", "\u2028", "\u2029"]
    html_text = text
    for char in newline_chars:
        html_text = re.sub(re.escape(char), "<br />", html_text)
    return html_text


def add_target_blank(html_content: str) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')
    for a_tag in soup.find_all('a'):
        a_tag['target'] = '_blank'

    return str(soup)


def get_display_created(d: datetime.datetime, user_preferences: UserPreferences) -> str:
    d = d.astimezone(datetime.timezone.utc)

    time_zone_offset = user_preferences.time_zone_offset
    assert len(time_zone_offset) == 5, "check time_zone_offset length!"
    current_date = datetime.date.today()
    offset_hours = int(time_zone_offset[1:3])
    offset_minutes = int(time_zone_offset[3:])
    offset_delta = datetime.timedelta(hours=offset_hours, minutes=offset_minutes)

    if time_zone_offset[0] == "-":
        adjusted_date = d - offset_delta
    else:
        adjusted_date = d + offset_delta

    if user_preferences.language == "ko":
        if adjusted_date.date() == current_date:
            time_string = format_time(adjusted_date, "a h:mm", locale="ko_KR")
            time_string = time_string.replace('AM', '오전').replace('PM', '오후')

        else:
            if adjusted_date.year == current_date.year:
                time_string = format_date(adjusted_date, "M월 d일", locale="ko_KR")
            else:
                time_string = format_date(adjusted_date, "yy. M. d.", locale="ko_KR")
    else:
        if adjusted_date.date() == current_date:
            time_string = format_time(adjusted_date, "h:mm a", locale="en_US")
        else:
            if adjusted_date.year == current_date.year:
                time_string = format_date(adjusted_date, "MMM d", locale="en_US")
            else:
                time_string = format_date(adjusted_date, "yy. M. d.", locale="en_US")

    return time_string


def get_static_file(platform_type: PlatformTypes, filename: str, language: str = "xx", color_theme="light") -> str:
    if platform_type == PlatformTypes.DESKTOP:
        extension = 'svg'
    else:
        extension = 'png'

    color_suffix = ''
    if color_theme != "light":
        color_suffix = color_theme

    return f'{settings.BASE_URL}/static/{extension}/{language}_{filename}{color_suffix}.{extension}'


def decode_charset(s: str):
    decoded_list = decode_header(s)
    decoded_address = ""
    for decoded_string, charset in decoded_list:
        if charset is not None:
            try:
                if isinstance(decoded_string, bytes):
                    decoded_address += decoded_string.decode(charset)
                else:
                    decoded_address += decoded_string
            except LookupError:
                if charset.lower() == 'ks_c_5601-1987':
                    if isinstance(decoded_string, bytes):
                        decoded_address += decoded_string.decode('euc_kr')
                    else:
                        decoded_address += decoded_string
        else:
            if isinstance(decoded_string, bytes):
                decoded_address += decoded_string.decode()
            else:
                decoded_address += decoded_string

    return decoded_address


def cid_to_datauri(email: Message):
    """
    Convert CID references in the HTML body to data URIs.
    """
    for part in email.walk():
        if part.get('Content-ID'):
            cid = part.get('Content-ID').strip('<>')
            if part.get_content_maintype() == 'image':
                image_data = part.get_payload(decode=True)
                image_data_b64 = base64.b64encode(image_data).decode('utf-8')
                content_type = part.get_content_type()
                data_uri = f'data:{content_type};base64,{image_data_b64}'

                yield cid, data_uri


def replace_cid_with_datauri(html, cid_to_datauri_mapping):
    """
    Replace CIDs in the HTML with the corresponding data URIs.
    """
    for cid, data_uri in cid_to_datauri_mapping:
        html = html.replace(f'cid:{cid}', data_uri)

    return html


def escape_email(email):
    return email.replace('<', '&lt;').replace('>', '&gt;').replace('"', '')
