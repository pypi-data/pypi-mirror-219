import base64
import datetime
import email
import re
from email.message import Message
from email.utils import parsedate_to_datetime
from typing import Any

from bs4 import BeautifulSoup
from pydantic import BaseModel

from action.schemas import UserPreferences
from imap.utils import decode_to_bytes_from_base64, create_html_content, \
    add_target_blank, get_display_created, decode_charset, cid_to_datauri, replace_cid_with_datauri, escape_email
from logger import get_logger


class Attachment(BaseModel):
    filename: str
    raw: bytes

    @property
    def extension(self) -> str:
        return self.filename.split('.')[-1]

    @property
    def file_size(self) -> int:
        return len(self.raw)


class EmailAddress(BaseModel):
    personal_name: str | None
    mailbox_name: str
    host_name: str


class EmailList(BaseModel):
    seq_num: int
    subject: str
    from_: list[dict] = []
    sender: list[dict] | None
    reply_to: list[dict] | None
    to: list[dict] = []
    message_id: str
    created: str
    snippet: str = ''
    flags: list[str] | None
    attachment: list[str] | None

    def __init__(self, **data):
        logger = get_logger("EmailList.init")

        if 'snippet' in data:
            try:
                s = base64.urlsafe_b64decode(data['snippet'])
                data['snippet'] = s.decode('UTF-8')
            except UnicodeDecodeError as e:
                data['snippet'] = ''
                # logger.error(str(e))
            except Exception as e:
                # logger.error(str(e))
                data['snippet'] = ''

        if 'from' in data:
            data['from_'] = data['from']

        subject_or_null = data.get('subject', None)
        if subject_or_null is None:
            data['subject'] = ''

        super().__init__(**data)

    @property
    def from_addresses(self) -> list[EmailAddress]:
        return [EmailAddress(**address_dict) for address_dict in self.from_]

    @property
    def reply_to_addresses(self) -> list[EmailAddress]:
        if self.reply_to:
            return [EmailAddress(**address_dict) for address_dict in self.reply_to]
        return []

    @property
    def to_addresses(self) -> list[EmailAddress]:
        return [EmailAddress(**address_dict) for address_dict in self.to]

    def get_created_time(self, user_preferences: UserPreferences) -> str:
        return get_display_created(
            datetime.datetime.strptime(self.created, '%Y-%m-%dT%H:%M:%S%z'), user_preferences)


class EmailDetail(BaseModel):
    message_id: str
    raw: str
    mail: Message
    size: int

    def __init__(__pydantic_self__, **data: Any) -> None:
        raw = data.get('raw', None)
        byte = decode_to_bytes_from_base64(raw)
        data['size'] = len(byte)
        data['mail'] = email.message_from_bytes(byte)
        super().__init__(**data)

    def get_created_time(self, user_preferences: UserPreferences) -> str:
        created_time: str = self.mail.get('Date')
        assert created_time, "check created_time !!"
        created_datetime: datetime = parsedate_to_datetime(created_time)
        return get_display_created(created_datetime, user_preferences)

    def add_header_and_attachment(
            self, html_content: str, user_preferences: UserPreferences, attachments: list[Attachment]) -> str:
        from config import settings
        created = self.get_created_time(user_preferences)
        style_content = f"""
            @font-face {{
                font-family: 'Inter Variable';
                font-weight: 1 999;
                font-style: oblique 0deg 10deg;
                font-display: swap;
            }}

            #swit-header {{
                padding: 8px;
            }}

            #swit-subject-content {{
                font-size: 20px;
                font-weight: 500;
                color: #424242;
                padding-bottom: 12px;
            }}

            #swit-toggle-content {{
                display: none;
                height: 126px;
                overflow: scroll;
                max-width: 330px;
                border-radius: 6px;
                padding: 8px 12px 8px 12px;
            }}

            #swit-toggle-checkbox:checked ~ #swit-toggle-content {{
                display: block;
            }}

            .swit-blur {{
                font-size: 14px;
                font-weight: 400;
                line-height: 22px;
                text-align: left;
                color: #959595;
            }}

            #swit-recipients {{
                max-width: 330px;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                display: inline-block;
            }}

            #swit-sender {{
                font-size: 14px;
                font-weight: 700;
                line-height: 22px;
                text-align: left;
                flex: 1;
            }}

            label::after {{
                content: url('{settings.BASE_URL}/static/svg/bottom_arrow.svg');
                display: inline-block;
                transform: translateY(1px);
            }}

            #swit-toggle-checkbox:checked ~ label::after {{
                content: url('{settings.BASE_URL}/static/svg/bottom_arrow_filled.svg');
            }}

            .swit-email-container {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                width: 330px;
            }}

            .swit-email-details {{
                display: flex;
                gap: 1px;
            }}

            .swit-email-attachment, .swit-email-time {{
                font-size: 10px;
                font-weight: 500;
                line-height: 16px;
                text-align: left;
                color: #757575;
                padding-left: 5px;
            }}
        """

        header_content = f"""
        <div id="swit-header">
            <div id="swit-subject-content">
                {self.subject}
            </div>
            <div class="swit-email-container">
                <div id="swit-sender">{self.sender}</div>
                <div class="swit-email-details">
                    {f'<div class="swit-email-attachment"><img src="{settings.BASE_URL}/static/svg/xx_ic_attachment_line_16attachment.svg" alt=""/></div>' if attachments and len(attachments) > 0 else ''}
                <div class="swit-email-time">
                    {created}
                </div>
            </div>
        </div>
        </div>
        """

        if self.recipients:
            recipients_content = f"""
            <span class="swit-blur" id="swit-recipients">
                {", ".join(self.recipients)}
            </span>
            <input type="checkbox" id="swit-toggle-checkbox" style="display: none;">
            <label for="swit-toggle-checkbox"></label>
            <div class="swit-blur" id="swit-toggle-content">
                {", ".join(self.recipients)}
            </div>
            </div>
            """
            header_content += recipients_content

        header_content += "</div>"

        soup = BeautifulSoup(html_content, 'html.parser')
        html = soup.html
        if html is None:
            html = soup.new_tag('html')
            soup.insert(0, html)

        head = soup.head
        if head is None:
            head = soup.new_tag('head')
            html.append(head)

        style = soup.find('style')
        if style is None:
            style = soup.new_tag('style')
            head.append(style)
            style.append(style_content)
        else:
            style.string += style_content

        style_tags = soup.find_all('style')
        for style in style_tags:
            # Remove CSS comments using a regex
            clean_css = re.sub(r'/\*.*?\*/', '', style.string, flags=re.DOTALL)
            # Replace the content of the style tag with the cleaned CSS
            style.string.replace_with(clean_css)

        header_soup = BeautifulSoup(header_content, 'html.parser')
        body = soup.find('body')
        if body is not None:
            body.insert(0, header_soup)
        else:
            head.insert_after(header_soup)

        return str(soup)

    def get_html(self, user_preferences: UserPreferences, attachments: list[Attachment]) -> str:
        html_content: str | None = None
        for part in self.mail.walk():
            if part.get_content_type() == "text/html":
                raw_payload = part.get_payload(decode=True)
                charset = part.get_content_charset()  # This will extract charset from the "Content-Type" header
                if charset is None:  # If charset is not defined in the header, fallback to utf-8
                    charset = "utf-8"

                try:
                    html_content = raw_payload.decode(charset)
                except UnicodeDecodeError:
                    try:
                        html_content = raw_payload.decode('utf-8')  # Try decoding with utf-8
                    except UnicodeDecodeError:
                        html_content = raw_payload.decode('latin-1')  # Fallback to latin-1 if utf-8 fails

                html_content = self.add_header_and_attachment(html_content, user_preferences, attachments)
                html_content = add_target_blank(html_content)
                cid_to_datauri_mapping = list(cid_to_datauri(self.mail))
                html_content = replace_cid_with_datauri(html_content, cid_to_datauri_mapping)
                break

        if html_content is None:
            for part in self.mail.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        html_content = part.get_payload(decode=True).decode("UTF-8")
                    except UnicodeDecodeError as e:
                        html_content = part.get_payload(decode=True).decode("latin-1")

                    html_content = create_html_content(html_content)
                    break

        assert html_content is not None, "text or html 이여만 한다 아니면 조짐"

        return html_content

    @property
    def subject(self) -> str:
        subject = self.mail.get('Subject')
        return decode_charset(subject)

    @property
    def attachments(self) -> list[Attachment]:
        ret: list[Attachment] = []
        for part in self.mail.walk():
            if part.get('Content-Disposition') is not None and part.get('Content-Disposition').startswith('attachment'):
                filename = part.get_filename()
                decoded_filename = decode_charset(filename)
                content = part.get_payload(decode=True)
                ret.append(Attachment(filename=decoded_filename, raw=content))

        return ret

    @property
    def recipients(self) -> list[str]:
        to: list[str] = self.mail.get_all('To', [])
        if len(to) == 0:
            return to

        decoded_to = []
        for address in to:
            decoded_address = decode_charset(address)
            decoded_to.append(decoded_address)

        recipients: list[str] = decoded_to[0].split(',')
        return [escape_email(recipient) for recipient in recipients]

    @property
    def sender(self) -> str:
        sender: str = self.mail.get('From')
        return escape_email(decode_charset(sender))

    class Config:
        arbitrary_types_allowed = True
