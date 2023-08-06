from action.constants import ActionIdTypes
from conversation import service as conversation_service
from conversation.schemas import Room
from lokalise import get_translated_text
from membership.schemas import OrganizationUser
from ui.common.Button import Button
from ui.common.StaticAction import StaticAction
from ui.draw_managers import ImapDrawManager
from ui.header.Header import Header
from ui.select.Option import Option
from ui.select.Select import Select
from ui.swit_response.Body import Body
from ui.swit_response.Footer import Footer
from ui.swit_response.SwitResponse import SwitResponse, ViewCallbackType
from ui.swit_response.View import View
from ui.text_paragraph.TextParagraph import TextParagraph
from ui.utils import add_action_id
from emails import service as email_service
from membership import service as membership_service


class ShareDmModalDrawManager(ImapDrawManager):
    async def draw(self) -> SwitResponse:
        assert self.state.email_detail_raw, "email_detail_raw is None !!"
        assert self.state.email_detail_message_id, "email_detail_message_id is None !!"
        assert self.state.workspace_id, "workspace_id is None !!"

        new_view = await self.build_view()

        return SwitResponse(
            callback_type=self.view_call_back_type,
            new_view=new_view
        )

    async def build_view(self) -> View:
        dm_text_paragraph = TextParagraph(
            content=get_translated_text(self.action_request.user_preferences.language, "sharetodm.title"))
        rooms: list[Room] = await conversation_service.get_all_rooms(self.action_request)
        org_users: list[OrganizationUser] = await membership_service.get_all_org_users(
            self.action_request, self.state.workspace_id)

        _hash: set = set()
        dm_options: list[Option] = []
        for room in rooms:
            _hash.add(room.room_or_user_id)
            dm_options.append(
                Option(
                    label=room.room_name,
                    action_id=add_action_id(
                        ActionIdTypes.select_room_on_share_to_dm_modal, room.room_or_user_id))
            )

        user_options: list[Option] = [
            Option(
                label=user.user_name,
                action_id=add_action_id(
                    ActionIdTypes.select_room_on_share_to_dm_modal, user.user_id
                ),
            )
            for user in org_users
            if user.user_id not in _hash
        ]

        rooms_select = Select(
            placeholder=get_translated_text(self.action_request.user_preferences.language, "to.label"),
            trigger_on_input=True,
            value=[''],
            options=dm_options + user_options,
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
            action_id=ActionIdTypes.share_to_dm,
            disabled=True
        )

        return View(
            view_id=self.view_id,
            state=self.state.to_bytes(),
            header=Header(
                title=get_translated_text(self.action_request.user_preferences.language, "sharetodm.title")
            ),
            body=Body(
                elements=[dm_text_paragraph, rooms_select]
            ),
            footer=Footer(buttons=[close_button, share_button])
        )


class RoomChangeDrawManager(ImapDrawManager):
    async def draw(self) -> SwitResponse:
        new_view = await self.build_view()

        return SwitResponse(
            callback_type=ViewCallbackType.update,
            new_view=new_view
        )

    async def build_view(self) -> View:
        convert_button: Button = self.action_request.current_view.footer.buttons[1]
        convert_button.disabled = False
        return self.action_request.current_view


class ShareCloseModalDrawManager(ImapDrawManager):
    async def draw(self) -> SwitResponse:
        assert self.state.workspace_id, "check workspace_id !!"
        assert self.state.email_detail_raw, "check email_detail_raw !!"

        current_view = self.action_request.current_view
        room_or_user_id: str = ActionIdTypes.get_action_value(current_view.body.elements[1].value[0])
        await email_service.share_to_dm(
            self.action_request, self.state.email_detail_raw, room_or_user_id)

        return SwitResponse(
            callback_type=self.view_call_back_type,
            new_view=self.action_request.current_view
        )

    async def build_view(self) -> View:
        pass
