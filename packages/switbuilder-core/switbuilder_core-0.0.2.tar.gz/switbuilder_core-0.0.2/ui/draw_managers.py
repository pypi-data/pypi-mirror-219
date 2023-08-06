import asyncio

from action.constants import ViewIdTypes, ActionIdTypes
from action.schemas import State, ActionRequest
from action.utils import get_file_type
from channel import service as channel_service
from config import settings
from imap import service as imap_service
from imap.constants import max_share_size
from imap.utils import get_static_file
from lokalise import get_translated_text
from ui.collection_entry.Background import Background
from ui.collection_entry.CollectionEntry import CollectionEntry
from ui.collection_entry.MetadataItem import MetadataItem
from ui.collection_entry.TextContent import TextContent
from ui.collection_entry.TextSection import TextSection
from ui.collection_entry.TextStyle import TextStyle
from ui.common.Button import Button
from ui.common.Icon import Icon
from ui.common.StaticAction import StaticAction
from ui.draw_manager_abc import DrawManagerABC
from ui.file.File import File
from ui.header.ContextMenuItem import ContextMenuItem
from ui.header.Header import Header
from ui.html_frame.HtmlFrame import HtmlFrame
from ui.image.Image import Image
from ui.input.Input import Input
from ui.select.Option import Option
from ui.select.Select import Select
from ui.select.Style import Style
from ui.signin.IntegratedService import IntegratedService
from ui.signin.SignInPage import SignInPage
from ui.swit_response.Body import Body
from ui.swit_response.Footer import Footer
from ui.swit_response.SwitResponse import SwitResponse, ViewCallbackType
from ui.swit_response.View import View
from ui.text_paragraph.TextParagraph import TextParagraph
from ui.utils import exclude_invalid_labels, add_action_id, get_attachment_query_param
from workspace import service as workspace_service


# noinspection PyAbstractClass
class ImapDrawManager(DrawManagerABC):

    def __init__(self,
                 action_request: ActionRequest,
                 state: State,
                 view_call_back_type: ViewCallbackType,
                 view_id: ViewIdTypes,
                 reference_view_id: ViewIdTypes | None = None,
                 new_state_data: dict | None = None):
        super().__init__(action_request, state, view_call_back_type, view_id, reference_view_id, new_state_data)
        self.action_request = action_request


class SignInDrawManager(DrawManagerABC):

    async def draw(self) -> SwitResponse:
        new_view = await self.build_view()
        return SwitResponse(
            callback_type=self.view_call_back_type,
            new_view=new_view,
            reference_view_id=self.reference_view_id
        )

    async def build_view(self) -> View:
        header = Header(
            title=get_translated_text(self.swit_request.user_preferences.language, "imap.appname"),
        )

        signin_page = SignInPage(
            integrated_service=IntegratedService(
                icon=Icon(
                    type='image',
                    image_url=settings.BASE_URL + '/static/png/app_image.png',
                    alt='string'
                )
            ),
            title=get_translated_text(self.swit_request.user_preferences.language, "Try.service.for.swit"),
            description=get_translated_text(self.swit_request.user_preferences.language, "connect.your.appname"),
            button=Button(
                label=get_translated_text(self.swit_request.user_preferences.language, "signin.button"),
                type='button',
                style="primary_filled",
                disabled=False,
                action_id="action_02",
                static_action=StaticAction(
                    action_type='open_oauth_popup',
                    link_url=settings.BASE_URL + '/auth/user'
                )
            )
        )

        body = Body(
            elements=[signin_page]
        )

        return View(
            view_id=self.view_id,
            state=self.state.to_bytes(),
            header=header,
            body=body
        )


class MailListDrawManager(ImapDrawManager):
    async def draw(self) -> SwitResponse:
        new_view = await self.build_view()

        return SwitResponse(
            callback_type=self.view_call_back_type,
            new_view=new_view,
            reference_view_id=self.reference_view_id
        )

    async def build_view(self) -> View:
        mails = await imap_service.get_mails(self.action_request, self.state)
        labels: list[str] = await imap_service.get_labels(self.action_request)
        valid_labels = exclude_invalid_labels(labels)

        assert len(valid_labels) >= 1, "label에 INBOX는 가져야지!!"

        if self.view_id == ViewIdTypes.right_panel:
            context_menu_item = ContextMenuItem(
                label=get_translated_text(self.action_request.user_preferences.language, "signout.title"),
                action_id=ActionIdTypes.open_logout_modal_from_right_panel)
        else:
            context_menu_item = ContextMenuItem(
                label=get_translated_text(self.action_request.user_preferences.language, "signout.title"),
                action_id=ActionIdTypes.open_logout_modal_from_action_modal)

        header = Header(
            title=get_translated_text(self.action_request.user_preferences.language, "imap.appname"),
            context_menu=[context_menu_item, ],
            buttons=[
                Button(
                    type='button',
                    label=ActionIdTypes.refresh,
                    action_id=ActionIdTypes.refresh,
                    icon=Icon(
                        type='image',
                        image_url=get_static_file(self.action_request.platform, 'reload',
                                                  color_theme=self.action_request.user_preferences.color_theme),
                        alt='Header button icon'
                    ),
                )
            ])

        input_ = Input(
            action_id=ActionIdTypes.search,
            placeholder=get_translated_text(self.action_request.user_preferences.language, "search.placeholder"),
            trigger_on_input=True,
            value=self.state.keyword if self.state.keyword else None
        )

        select = Select(
            trigger_on_input=True,
            value=[
                add_action_id(ActionIdTypes.select_label, self.state.label)
            ],
            options=[
                Option(
                    label=label,
                    action_id=add_action_id(ActionIdTypes.select_label, label))
                for label in valid_labels
            ],
            style=Style(variant="ghost")
        )

        items = []
        for mail in mails:
            has_attachment = mail.attachment is not None
            is_read: bool = mail.flags is None

            text_section1 = TextSection(
                text=TextContent(
                    content=mail.from_addresses[0].personal_name or
                            mail.from_addresses[0].mailbox_name or
                            mail.from_addresses[0].host_name,
                    style=TextStyle(
                        bold=True if is_read else False,
                        color="gray900",
                        size="large",
                        max_lines=1
                    )
                ),
                metadata_items=[
                    MetadataItem(
                        type="subtext",
                        content=mail.get_created_time(self.action_request.user_preferences)
                    ),
                ]
            )

            if has_attachment:
                text_section1.metadata_items.append(
                    MetadataItem(
                        type="image",
                        image_url=get_static_file(self.action_request.platform, "ic_attachment_line_16attachment"),
                    ),
                )

            text_section2 = TextSection(
                text=TextContent(
                    content=mail.subject,
                    style=TextStyle(
                        bold=False,
                        color="gray800",
                        size="medium",
                        max_lines=1
                    )
                ),
            )

            text_section3 = None
            if mail.snippet:
                text_section3 = TextSection(
                    text=TextContent(
                        content=mail.snippet,
                        style=TextStyle(
                            bold=False,
                            color="gray700",
                            size="medium",
                            max_lines=1
                        )
                    ),
                )

            text_sections = [text_section1, text_section2]

            if text_section3:
                text_sections.append(text_section3)

            if self.view_id == ViewIdTypes.right_panel:
                action_id = add_action_id(ActionIdTypes.go_to_mail_detail, mail.message_id)
            else:
                action_id = add_action_id(ActionIdTypes.share_to_channel_from_action_modal, mail.message_id)

            c = CollectionEntry(
                text_sections=text_sections,
                vertical_alignment="middle",
                background=Background(color="lightblue" if is_read else "none"),
                action_id=action_id,
                draggable=True
            )

            items.append(c)

        is_empty: bool = len(items) == 0
        if is_empty:
            if self.state.keyword:
                filename = "search_empty"
            else:
                filename = "empty"
            items.append(
                Image(
                    image_url=get_static_file(self.action_request.platform, filename,
                                              self.action_request.user_preferences.language))
            )

        body = Body(elements=[input_, select, *items])

        footer_or_null: Footer | None = None
        if self.state.seq > 1:
            prev_button = Button(
                type='button',
                label=get_translated_text(self.action_request.user_preferences.language, "see.previous"),
                style="secondary",
                action_id=ActionIdTypes.prev_page,
            )
            footer_or_null = Footer(buttons=[prev_button])

        if not is_empty:
            prev_button = Button(
                type='button',
                label=get_translated_text(self.action_request.user_preferences.language, "see.previous"),
                style="secondary",
                action_id=ActionIdTypes.prev_page,
                disabled=True if self.state.seq == 1 else False
            )

            next_button = Button(
                type='button',
                label=get_translated_text(self.action_request.user_preferences.language, "see.next"),
                style="secondary",
                action_id=ActionIdTypes.next_page,
                disabled=True if len(mails) < self.state.limit else False
            )

            footer_or_null = Footer(buttons=[prev_button, next_button])

        return View(
            view_id=self.view_id,
            state=self.state.to_bytes(),
            header=header,
            body=body,
            footer=footer_or_null if footer_or_null else None
        )


class BackToMailListDrawManager(ImapDrawManager):
    async def draw(self) -> SwitResponse:
        assert self.state.email_list_view, "BackToMailList must have email_list_view state!!"
        new_view = await self.build_view()

        return SwitResponse(
            callback_type=self.view_call_back_type,
            new_view=new_view,
            reference_view_id=self.reference_view_id
        )

    async def build_view(self) -> View:
        email_list_view = View(**self.state.email_list_view)
        for element in email_list_view.body.elements:
            if getattr(element, "action_id", "") == self.state.email_action_id:
                assert isinstance(element, CollectionEntry), "emails list type is CollectionEntry"
                element.background.color = "none"
                element.text_sections[0].text.style.bold = False
                break

        return email_list_view


class ShareModalDrawManager(ImapDrawManager):
    async def draw(self) -> SwitResponse:
        new_view = await self.build_view()

        return SwitResponse(
            callback_type=self.view_call_back_type,
            new_view=new_view,
            reference_view_id=self.reference_view_id
        )

    async def build_view(self) -> View:
        workspace_id = self.action_request.context.workspace_id or self.state.workspace_id
        channel_id = self.action_request.context.channel_id or self.state.channel_id

        assert workspace_id, "context must have workspace_id!!"

        workspaces = await workspace_service.get_all_workspaces_recursive(self.action_request)
        current_workspace = workspace_service.get_workspace(workspaces, workspace_id)
        channels = await channel_service.get_all_channels_recursive(self.action_request, current_workspace.id)
        current_or_null = channel_service.get_channel_or_null(channels, channel_id)

        workspace_text_paragraph = TextParagraph(
            markdown=False, content=get_translated_text(self.action_request.user_preferences.language, "workspace"))
        workspace_select = Select(
            placeholder="Select workspace",  # TODO Lokalise
            trigger_on_input=True,
            value=[
                add_action_id(ActionIdTypes.select_workspace_on_share_modal, current_workspace.id)
            ],
            options=[
                Option(
                    label=workspace.name,
                    action_id=add_action_id(ActionIdTypes.select_workspace_on_share_modal, workspace.id))
                for workspace in workspaces
            ],
        )

        channel_text_paragraph = TextParagraph(
            markdown=False,
            content=get_translated_text(self.action_request.user_preferences.language, "sharetochannel.channel"))
        channel_select = Select(
            placeholder="Select Channel",  # TODO Lokalise
            trigger_on_input=True,
            value=[
                add_action_id(ActionIdTypes.select_channel_on_share_modal,
                              current_or_null.id) if current_or_null else ''
            ],
            options=[
                Option(
                    label=channel.name,
                    action_id=add_action_id(ActionIdTypes.select_channel_on_share_modal, channel.id))
                for channel in channels
            ],
        )

        close_button = Button(
            label=get_translated_text(self.action_request.user_preferences.language, "cancel.button"),
            style="primary",
            static_action=StaticAction(
                action_type="close_view"
            )
        )

        share_button = Button(
            label=get_translated_text(self.action_request.user_preferences.language, "send.sharetochannel.button"),
            style="primary_filled",
            disabled=(current_or_null is None),
            action_id=ActionIdTypes.share_and_close_modal
        )

        return View(
            view_id=self.view_id,
            state=self.state.to_bytes(),
            header=Header(
                title=get_translated_text(self.action_request.user_preferences.language, "sharetochannel.title")
            ),
            body=Body(
                elements=[workspace_text_paragraph, workspace_select, channel_text_paragraph, channel_select]
            ),
            footer=Footer(buttons=[close_button, share_button])
        )


class WorkspaceChangeModalDrawManager(ImapDrawManager):
    async def draw(self) -> SwitResponse:
        new_view = await self.build_view()

        return SwitResponse(
            callback_type=self.view_call_back_type,
            new_view=new_view,
            reference_view_id=self.reference_view_id
        )

    async def build_view(self) -> View:
        current_view: View = self.action_request.current_view
        assert current_view, "current_view check!!"

        workspace_id = None
        for element in self.action_request.current_view.body.elements:
            if isinstance(element, Select):
                workspace_id = ActionIdTypes.get_action_value(element.value[0])
                break

        channels = await channel_service.get_all_channels_recursive(self.action_request, workspace_id)

        channel_select = Select(
            placeholder="Select Channel",  # TODO Lokalise
            trigger_on_input=True,
            options=[
                Option(
                    label=channel.name,
                    action_id=add_action_id(ActionIdTypes.select_channel_on_share_modal, channel.id))
                for channel in channels
            ],
        )

        current_view.body.elements[3] = channel_select
        submit_button: Button = self.action_request.current_view.footer.buttons[1]
        submit_button.disabled = True
        assert workspace_id is not None, "workspace_id check!!"
        return current_view


class ChannelChangeModalDrawManager(ImapDrawManager):
    async def draw(self) -> SwitResponse:
        new_view = await self.build_view()

        return SwitResponse(
            callback_type=self.view_call_back_type,
            new_view=new_view,
            reference_view_id=self.reference_view_id
        )

    async def build_view(self) -> View:
        current_view: View = self.action_request.current_view
        assert current_view, "current_view check!!"
        submit_button: Button = self.action_request.current_view.footer.buttons[1]
        submit_button.disabled = False

        return current_view


class MailDetailDrawManager(ImapDrawManager):

    async def draw(self) -> SwitResponse:
        new_view = await self.build_view()

        return SwitResponse(
            callback_type=self.view_call_back_type,
            new_view=new_view,
            reference_view_id=self.reference_view_id
        )

    async def build_view(self) -> View:
        mail = await imap_service.get_mail(
            self.action_request, ActionIdTypes.get_action_value(self.action_request.user_action.id))

        self.state = self.state.update(
            {
                "email_list_view": self.action_request.current_view.dict(),
                "email_action_id": self.action_request.user_action.id,
                "email_detail_raw": mail.raw,
                "email_detail_message_id": mail.message_id,
            })

        asyncio.create_task(imap_service.read(self.action_request, mail.message_id, self.state.label))

        header = Header(
            title=get_translated_text(self.action_request.user_preferences.language, "imap.appname"),
            context_menu=[
                ContextMenuItem(
                    label=get_translated_text(self.action_request.user_preferences.language, "sharetochannel.title"),
                    action_id=add_action_id(ActionIdTypes.share_to_channel_from_detail, mail.message_id)),
                # ContextMenuItem(
                #     label=get_translated_text(self.action_request.user_prefer리ences.language, "sharetodm.title"),
                #     action_id=ActionIdTypes.open_share_to_dm_modal),
                # ContextMenuItem(
                #     label=get_translated_text(self.action_request.user_preferences.language, "attachtotask.title"),
                #     action_id=ActionIdTypes.open_attach_to_task_modal),
                # ContextMenuItem(
                #     label=get_translated_text(self.action_request.user_preferences.language, "converttask.title"),
                #     action_id=ActionIdTypes.open_convert_to_task_modal),
            ])

        attachment: list[File] = []
        attachments = mail.attachments
        for i in range(len(attachments)):
            attachment.append(
                File(
                    file_name=attachments[i].filename,
                    file_size=attachments[i].file_size,
                    file_type=get_file_type(attachments[i].extension),
                    action_id=ActionIdTypes.download_file,
                    static_action=StaticAction(
                        action_type='open_link',
                        link_url=f'{settings.BASE_URL}/action/attachment?{get_attachment_query_param(mail.message_id, i, self.action_request.user.swit_id)}'
                    )
                )
            )

        email_body_html_frame = HtmlFrame(
            html_content=mail.get_html(self.action_request.user_preferences, attachments))

        body = Body(
            elements=[email_body_html_frame, *attachment]
        )

        back_button = Button(
            label=get_translated_text(self.action_request.user_preferences.language, "gobacktomails.button"),
            style="secondary",
            action_id=ActionIdTypes.back_to_mail_list
        )

        return View(
            view_id=ViewIdTypes.right_panel,
            state=self.state.to_bytes(),
            header=header,
            body=body,
            footer=Footer(buttons=[back_button])
        )


class LogoutModalDrawManager(ImapDrawManager):
    async def draw(self) -> SwitResponse:
        new_view = await self.build_view()

        return SwitResponse(
            callback_type=self.view_call_back_type,
            new_view=new_view
        )

    async def build_view(self) -> View:
        if self.view_call_back_type == ViewCallbackType.update:
            close_button = Button(
                label=get_translated_text(self.action_request.user_preferences.language, "cancel.button"),
                style="primary",
                action_id=ActionIdTypes.close_logout_modal
            )
            sign_out_button = Button(
                label=get_translated_text(self.action_request.user_preferences.language, "signout.title"),
                style="primary_filled",
                action_id=ActionIdTypes.logout_from_modal
            )

        else:
            close_button = Button(
                label=get_translated_text(self.action_request.user_preferences.language, "cancel.button"),
                style="primary",
                static_action=StaticAction(
                    action_type="close_view"
                )
            )
            sign_out_button = Button(
                label=get_translated_text(self.action_request.user_preferences.language, "signout.title"),
                style="primary_filled",
                action_id=ActionIdTypes.logout_from_right_panel
            )

        text_paragraph = TextParagraph(
            content=get_translated_text(self.action_request.user_preferences.language, "signout.body")
        )

        return View(
            view_id=self.view_id,
            state=self.state.to_bytes(),
            header=Header(
                title=get_translated_text(self.action_request.user_preferences.language, "signout.title")
            ),
            body=Body(
                elements=[text_paragraph]
            ),
            footer=Footer(buttons=[close_button, sign_out_button])
        )


class MailListFromStateDrawManager(ImapDrawManager):
    async def draw(self) -> SwitResponse:
        assert self.state.email_list_view, "MailListFromStateDrawManager must have email_list_view state !!"

        new_view = await self.build_view()

        return SwitResponse(
            callback_type=ViewCallbackType.update,
            new_view=new_view
        )

    async def build_view(self) -> View:
        return View(**self.state.email_list_view)


class ShareCloseDrawManager(ImapDrawManager):

    async def draw(self) -> SwitResponse:
        assert self.state.shared_email_id, "check shared_email_id !!"
        message_id = ActionIdTypes.get_action_value(self.state.shared_email_id)
        email = await imap_service.get_mail(self.action_request, message_id)

        if email.size >= max_share_size:
            new_view = await self.build_cannot_share_modal()
            return SwitResponse(
                callback_type=ViewCallbackType.update,
                new_view=new_view
            )

        workspace_id = None
        channel_id = None

        for element in self.action_request.current_view.body.elements:
            if isinstance(element, Select):
                if workspace_id is None and channel_id is None:
                    workspace_id = ActionIdTypes.get_action_value(element.value[0])
                else:
                    channel_id = ActionIdTypes.get_action_value(element.value[0])

        assert workspace_id is not None
        assert channel_id is not None

        await imap_service.share_to_channel(self.action_request, email, workspace_id, channel_id)

        new_view = await self.build_view()

        return SwitResponse(
            callback_type=ViewCallbackType.close,
            new_view=self.action_request.current_view
        )

    async def build_view(self) -> View:
        pass

    async def build_cannot_share_modal(self) -> View:
        close_button = Button(
            label=get_translated_text(self.action_request.user_preferences.language, "close.button"),
            style="primary",
            static_action=StaticAction(
                action_type="close_view"
            )
        )

        text_paragraph = TextParagraph(
            content=get_translated_text(self.action_request.user_preferences.language, "emailsover7mb")
        )

        return View(
            view_id=self.view_id,
            state=self.state.to_bytes(),
            header=Header(
                title=get_translated_text(self.action_request.user_preferences.language, "unabletoshare.title")
            ),
            body=Body(
                elements=[text_paragraph]
            ),
            footer=Footer(buttons=[close_button])
        )
