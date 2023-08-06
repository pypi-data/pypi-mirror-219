import json
import os
import unittest

from bs4 import BeautifulSoup

from action.schemas import UserPreferences
from imap.schemas import EmailList, EmailDetail, Attachment
from imap.utils import cid_to_datauri, replace_cid_with_datauri

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)
email_dir = os.path.join(current_dir, 'email')
html_dir = os.path.join(current_dir, 'html')


# noinspection PyMethodMayBeStatic
class EmailLoadTest(unittest.TestCase):
    def create_user_preferences(self):
        return UserPreferences(language="ko", time_zone_offset="+0900", color_theme="light")

    def test_email_list(self):
        mails = [
            {
                "seq_num": 50,
                "subject": "[GitHub] A third-party OAuth application has been added to your account",
                "from": [
                    {
                        "personal_name": "GitHub",
                        "mailbox_name": "noreply",
                        "host_name": "github.com"
                    }
                ],
                "sender": [
                    {
                        "personal_name": "GitHub",
                        "mailbox_name": "noreply",
                        "host_name": "github.com"
                    }
                ],
                "reply_to": [
                    {
                        "personal_name": "GitHub",
                        "mailbox_name": "noreply",
                        "host_name": "github.com"
                    }
                ],
                "to": [
                    {
                        "personal_name": "Ellee12",
                        "mailbox_name": "el.lee",
                        "host_name": "swit.io"
                    }
                ],
                "message_id": "<6421545b3fa7e_529c9046537b@lowworker-5d549f48-2mclc.mail>",
                "created": "2023-03-27T08:31:23Z",
                "snippet": "SGV5IEVsbGVlMTIhIEEgdGhpcmQtcGFydHkgT0F1dGggYXBwbGljYXRpb24gKEpldEJyYWlucyBJREUgSW50ZWdyYXRpb24pIHdpdGggZ2lzdCwgcmVhZDpvcmcsIHJlcG8sIGFuZCB3b3JrZmxvdyBzY29wZXMgd2FzIHJlY2VudGx5IGF1dGhvcml6ZWQgdG8gYWNjZXNzIHlvdXIgYWNjb3VudC4gVmlzaXQgaHR0cHM6Ly9naXRodWIuY29tL3NldHRpbmdzL2Nvbm5lY3Rpb25zL2FwcGxpY2F0aW9ucy81ODU2Njg2MmJkMmE1ZmY3NDhmYiBmb3IgbW9yZSBpbmZvcm1hdGlvbi4gVG8gc2VlIHRoaXMgYW5kIG90aGVyIHNlY3VyaXR5IGV2ZW50cyBmb3IgeW91ciBhY2NvdW50LCB2aXNpdCBodHRwczovL2dpdGh1Yi5jb20vc2V0dGluZ3Mvc2VjdXJpdHktbG9nIElmIHlvdSBydW4gaW50byBwcm9ibGVtcywgcGxlYXNlIGNvbnRhY3Qgc3VwcG9ydCBieSB2aXNpdGluZyBodHRwczovL2dpdGh1Yi5jb20vY29udGFjdCBUaGFua3MsIFRoZSBHaXRIdWIgVGVhbQ==",
                "flags": [
                    "\\Seen"
                ]
            },
            {
                "seq_num": 49,
                "subject": "Reminder: Complete your security tasks",
                "from": [
                    {
                        "personal_name": "Vanta",
                        "mailbox_name": "no-reply",
                        "host_name": "vanta.com"
                    }
                ],
                "sender": [
                    {
                        "personal_name": "Vanta",
                        "mailbox_name": "no-reply",
                        "host_name": "vanta.com"
                    }
                ],
                "reply_to": [
                    {
                        "personal_name": "Vanta",
                        "mailbox_name": "no-reply",
                        "host_name": "vanta.com"
                    }
                ],
                "to": [
                    {
                        "mailbox_name": "el.lee",
                        "host_name": "swit.io"
                    }
                ],
                "in_reply_to": "<1f8d1f23-fc63-46d2-80ac-e2eeb9214c9c@vanta.com>",
                "message_id": "<0100018721f928f3-a52a1d8f-f6ad-46ed-a8e7-271eaf132736-000000@emails.amazonses.com>",
                "created": "2023-03-27T07:29:50Z",
                "snippet": "RWwsIFN3aXQgaGFzIHBhcnRuZXJlZCB3aXRoIFZhbnRhIHRvIGtlZXAgdGhlbSBzZWN1cmUgYW5kIGNvbXBsaWFudC4gWW91IGhhdmUgb3V0c3RhbmRpbmcgdGFza3MgdGhhdCByZXF1aXJlIHlvdXIgYXR0ZW50aW9uLiAtLS0tIFNlY3VyaXR5IHRhc2tzIOKAoiBJbnN0YWxsIFZhbnRhIGFnZW50VmlldyB0YXNrcyAoaHR0cHM6Ly9hcHAudmFudGEuY29tL2VtcGxveWVlL29uYm9hcmRpbmc_dXRtX2NhbXBhaWduPUVtcGxveWVlRGlnZXN0JnV0bV9tZWRpdW09ZW1haWwmdXRtX3NvdXJjZT1vcGVyYXRpb25hbCkgLS0tLSBIYXZlIGEgcXVlc3Rpb24gb3IgbmVlZCBhc3Npc3RhbmNlPyBTZW5kIHVzIGFuIGVtYWlsIGF0IHN1cHBvcnRAdmFudGEuY29tIC0tIFZhbnRhIHRlYW0gVmFudGEgKGh0dHBzOi8vYXBwLnZhbnRhLmNvbSkgfCBTZWN1cml0eSBhbmQgY29tcGxpYW5jZSBmb3IgaW50ZXJuZXQgYnVzaW5lc3Nlcw==",
                "flags": [
                    "\\Seen"
                ]
            }
        ]
        snippet1 = "Hey Ellee12! A third-party OAuth application (JetBrains IDE Integration) with gist, read:org, repo, and workflow scopes was recently authorized to access your account. Visit https://github.com/settings/connections/applications/58566862bd2a5ff748fb for more information. To see this and other security events for your account, visit https://github.com/settings/security-log If you run into problems, please contact support by visiting https://github.com/contact Thanks, The GitHub Team"
        snippet2 = "El, Swit has partnered with Vanta to keep them secure and compliant. You have outstanding tasks that require your attention. ---- Security tasks • Install Vanta agentView tasks (https://app.vanta.com/employee/onboarding?utm_campaign=EmployeeDigest&utm_medium=email&utm_source=operational) ---- Have a question or need assistance? Send us an emails at support@vanta.com -- Vanta team Vanta (https://app.vanta.com) | Security and compliance for internet businesses"
        email_lists: list[EmailList] = [EmailList(**data) for data in mails]
        self.assertEqual(len(email_lists), len(mails))
        self.assertEqual(email_lists[0].snippet, snippet1)
        self.assertEqual(email_lists[1].snippet, snippet2)
        self.assertEqual(len(email_lists[0].from_addresses), 1)

    def test_email_list_without_subject(self):
        mails = [
            {
                "seq_num": 49,
                "from": [
                    {
                        "personal_name": "Vanta",
                        "mailbox_name": "no-reply",
                        "host_name": "vanta.com"
                    }
                ],
                "sender": [
                    {
                        "personal_name": "Vanta",
                        "mailbox_name": "no-reply",
                        "host_name": "vanta.com"
                    }
                ],
                "reply_to": [
                    {
                        "personal_name": "Vanta",
                        "mailbox_name": "no-reply",
                        "host_name": "vanta.com"
                    }
                ],
                "to": [
                    {
                        "mailbox_name": "el.lee",
                        "host_name": "swit.io"
                    }
                ],
                "in_reply_to": "<1f8d1f23-fc63-46d2-80ac-e2eeb9214c9c@vanta.com>",
                "message_id": "<0100018721f928f3-a52a1d8f-f6ad-46ed-a8e7-271eaf132736-000000@emails.amazonses.com>",
                "created": "2023-03-27T07:29:50Z",
                "snippet": "RWwsIFN3aXQgaGFzIHBhcnRuZXJlZCB3aXRoIFZhbnRhIHRvIGtlZXAgdGhlbSBzZWN1cmUgYW5kIGNvbXBsaWFudC4gWW91IGhhdmUgb3V0c3RhbmRpbmcgdGFza3MgdGhhdCByZXF1aXJlIHlvdXIgYXR0ZW50aW9uLiAtLS0tIFNlY3VyaXR5IHRhc2tzIOKAoiBJbnN0YWxsIFZhbnRhIGFnZW50VmlldyB0YXNrcyAoaHR0cHM6Ly9hcHAudmFudGEuY29tL2VtcGxveWVlL29uYm9hcmRpbmc_dXRtX2NhbXBhaWduPUVtcGxveWVlRGlnZXN0JnV0bV9tZWRpdW09ZW1haWwmdXRtX3NvdXJjZT1vcGVyYXRpb25hbCkgLS0tLSBIYXZlIGEgcXVlc3Rpb24gb3IgbmVlZCBhc3Npc3RhbmNlPyBTZW5kIHVzIGFuIGVtYWlsIGF0IHN1cHBvcnRAdmFudGEuY29tIC0tIFZhbnRhIHRlYW0gVmFudGEgKGh0dHBzOi8vYXBwLnZhbnRhLmNvbSkgfCBTZWN1cml0eSBhbmQgY29tcGxpYW5jZSBmb3IgaW50ZXJuZXQgYnVzaW5lc3Nlcw==",
                "flags": [
                    "\\Seen"
                ]
            }
        ]
        email_lists: list[EmailList] = [EmailList(**data) for data in mails]
        self.assertEqual(len(email_lists), len(mails))
        self.assertEqual(email_lists[0].subject, '')

    def test_html_email_detail(self):
        with open(email_dir + '/html_email.json', 'r') as file:
            data = json.load(file)
            mail = data["data"]['mail_detail']
            email_detail = EmailDetail(**mail)
            # self.assertIsInstance(email_detail.get_html(timezone='+0900'), str)
            self.assertEqual(len(email_detail.recipients), 1)
            self.assertIsNotNone(email_detail.sender)

    def test_plain_text_email_detail(self):
        with open(email_dir + '/plain_text_email.json', 'r') as file:
            data = json.load(file)
            mail = data["data"]['mail_detail']
            email_detail = EmailDetail(**mail)
            # self.assertIsInstance(email_detail.get_html(timezone='+0900'), str)
            self.assertEqual(len(email_detail.recipients), 1)
            self.assertIsNotNone(email_detail.sender)

    def test_attachment_email_detail(self):
        with open(email_dir + '/email_with_attachment.json', 'r') as file:
            data = json.load(file)
            mail = data["data"]['mail_detail']
            email_detail = EmailDetail(**mail)
            self.assertEqual(len(email_detail.attachments), 2)
            self.assertIsInstance(email_detail.attachments[0], Attachment)
            self.assertEqual(len(email_detail.recipients), 1)
            self.assertIsNotNone(email_detail.sender)
            self.assertGreater(email_detail.size, 1024 * 1024)

    def test_attachment_cid_image_email_detail(self):
        with open(email_dir + '/cid_image_email.json', 'r') as file:
            data = json.load(file)
            mail = data["data"]['mail_detail']
            email_detail = EmailDetail(**mail)
            self.assertIsInstance(email_detail.get_html(
                self.create_user_preferences(), email_detail.attachments), str)

            cid_to_datauri_mapping = list(cid_to_datauri(email_detail.mail))
            html_with_datauri = replace_cid_with_datauri(email_detail.get_html(self.create_user_preferences(), email_detail.attachments),
                                                         cid_to_datauri_mapping)
            self.assertIsNotNone(html_with_datauri)

    def test_large_cid_image_email_detail(self):
        with open(email_dir + '/large_cid_image_email.json', 'r') as file:
            data = json.load(file)
            mail = data["data"]['mail_detail']
            email_detail = EmailDetail(**mail)
            self.assertIsInstance(email_detail.get_html(self.create_user_preferences(), email_detail.attachments), str)

            cid_to_datauri_mapping = list(cid_to_datauri(email_detail.mail))
            html_with_datauri = replace_cid_with_datauri(email_detail.get_html(self.create_user_preferences(), email_detail.attachments),
                                                         cid_to_datauri_mapping)
            self.assertIsNotNone(html_with_datauri)

    def test_empty_receiver_email_detail(self):
        with open(email_dir + '/empty_receiver_email.json', 'r') as file:
            data = json.load(file)
            mail = data["data"]['mail_detail']
            email_detail = EmailDetail(**mail)
            self.assertEqual(len(email_detail.recipients), 1)

    def test_invalid_swit_image_email_detail(self):
        with open(email_dir + '/invalid_swit_image.json', 'r') as file:
            data = json.load(file)
            mail = data["data"]['mail_detail']
            email_detail = EmailDetail(**mail)
            self.assertIsNotNone(email_detail)


class HtmlTest(unittest.TestCase):
    def test_with_header_body_html(self):
        with open(html_dir + '/example1.html', 'r') as file:
            # head, body 있는 완전한 html 파일 테스트
            soup = BeautifulSoup(file, 'html.parser')
            for a_tag in soup.find_all('a'):
                # Add target="_blank" attribute
                a_tag['target'] = '_blank'

            html_content = soup.prettify()
        self.assertEqual(1, 1)
        # self.assertIsNotNone(head_tag, "The <head> tag is missing.")

    def test_add_bootstrap(self):
        with open(html_dir + '/example1.html', 'r') as file:
            soup = BeautifulSoup(file, 'html.parser')
            head_tag_or_null = soup.find('head')
            body_tag_or_null = soup.find('body')

            if not head_tag_or_null:
                head_tag = soup.new_tag('head')
                soup.html.insert(0, head_tag)

            if not body_tag_or_null:
                body_tag = soup.new_tag('body')
                soup.html.append(body_tag)

            # Create a new <link> tag for the Bootstrap CDN
            bootstrap_cdn_link = soup.new_tag('link')
            bootstrap_cdn_link['rel'] = 'stylesheet'
            bootstrap_cdn_link[
                'href'] = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css'

            # Find the <head> tag in the HTML document
            head_tag = soup.find('head')
            head_tag.append(bootstrap_cdn_link)

            # Create a new <button> tag
            button_tag = soup.new_tag('button')
            button_tag['type'] = 'button'
            button_tag['class'] = 'btn btn-primary'
            button_tag.string = 'Click me'

            # Append the <button> tag to the HTML body
            soup.body.append(button_tag)
            # Append the Bootstrap CDN link to the <head> tag

            self.assertEqual(1, 1)
