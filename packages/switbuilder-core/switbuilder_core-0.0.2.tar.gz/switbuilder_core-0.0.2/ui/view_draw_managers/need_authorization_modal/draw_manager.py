from action.constants import ActionIdTypes, ViewIdTypes
from config import settings
from emails import service as email_service
from lokalise import get_translated_text
from ui.common.Button import Button
from ui.common.StaticAction import StaticAction
from ui.draw_managers import ImapDrawManager
from ui.header.Header import Header
from ui.swit_response.Body import Body
from ui.swit_response.Footer import Footer
from ui.swit_response.SwitResponse import SwitResponse, ViewCallbackType
from ui.swit_response.View import View
from ui.text_paragraph.TextParagraph import TextParagraph


class NeedScopeModalDrawManager(ImapDrawManager):

    @property
    def is_modal(self) -> bool:
        if self.view_id == ViewIdTypes.right_panel:
            return False
        return True

    @property
    def _view_call_back_type(self) -> ViewCallbackType:
        if self.is_modal:
            view_call_back_type = ViewCallbackType.update
        else:
            view_call_back_type = ViewCallbackType.open

        return view_call_back_type

    @property
    def _view_id(self) -> ViewIdTypes:
        if self.is_modal:
            view_id = self.view_id
        else:
            view_id = ViewIdTypes.need_authorization_modal

        return view_id

    async def draw(self) -> SwitResponse:
        new_view = await self.build_view()

        view_call_back_type: ViewCallbackType

        return SwitResponse(
            callback_type=self._view_call_back_type,
            new_view=new_view
        )

    async def build_view(self) -> View:
        text_paragraph = TextParagraph(
            content=get_translated_text(self.action_request.user_preferences.language, "to.use.this.feature.authorize"))

        if self.is_modal:
            close_button = Button(
                label=get_translated_text(self.action_request.user_preferences.language, "cancel.button"),
                style="primary",
                action_id=ActionIdTypes.close_need_scope_modal
            )
        else:
            close_button = Button(
                label=get_translated_text(self.action_request.user_preferences.language, "cancel.button"),
                style="primary",
                static_action=StaticAction(
                    action_type="close_view"
                )
            )

        submit_button = Button(
            label=get_translated_text(self.action_request.user_preferences.language, "authroize.button"),
            type='button',
            style="primary_filled",
            action_id="action_01",
            static_action=StaticAction(
                action_type='open_oauth_popup',
                link_url=settings.BASE_URL + '/auth/authorize'
            )
        )

        return View(
            view_id=self._view_id,
            state=self.state.to_bytes(),
            header=Header(
                title=get_translated_text(self.action_request.user_preferences.language, "authorization.required.title")
            ),
            body=Body(
                elements=[text_paragraph]
            ),
            footer=Footer(buttons=[close_button, submit_button])
        )


class ShareCloseModalDrawManager(ImapDrawManager):
    async def draw(self) -> SwitResponse:
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


class PrevViewDrawManager(ImapDrawManager):
    async def draw(self) -> SwitResponse:
        assert self.state.prev_view, "check prev_view !!"

        return SwitResponse(
            callback_type=self.view_call_back_type,
            new_view=View(**self.state.prev_view)
        )

    async def build_view(self) -> View:
        pass
