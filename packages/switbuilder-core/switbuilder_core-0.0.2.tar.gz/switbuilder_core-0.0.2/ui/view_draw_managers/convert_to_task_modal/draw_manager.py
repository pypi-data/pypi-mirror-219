from action.constants import ActionIdTypes
from imap.schemas import EmailDetail
from lokalise import get_translated_text
from project.schemas import Project
from ui.common.Button import Button
from ui.common.StaticAction import StaticAction
from ui.draw_managers import ImapDrawManager
from ui.header.Header import Header
from ui.input.Input import Input
from ui.select.Option import Option
from ui.select.Select import Select
from ui.swit_response.Body import Body
from ui.swit_response.Footer import Footer
from ui.swit_response.SwitResponse import SwitResponse, ViewCallbackType
from ui.swit_response.View import View
from ui.text_paragraph.TextParagraph import TextParagraph
from ui.textarea.Textarea import Textarea, SizeTypes
from ui.utils import add_action_id
from project import service as project_service
from task import service as task_service
from workspace import service as workspace_service


class ConvertTaskModalDrawManager(ImapDrawManager):
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
        email_detail = EmailDetail(
            raw=self.state.email_detail_raw, message_id=self.state.email_detail_message_id)
        workspace_text_paragraph = TextParagraph(content="Workspace")
        workspaces = await workspace_service.get_all_workspaces_recursive(
            self.action_request)
        workspace_select = Select(
            placeholder=get_translated_text(self.action_request.user_preferences.language, "link.placeholder"),
            trigger_on_input=True,
            value=[add_action_id(
                ActionIdTypes.select_workspace_on_convert_new_task_modal, self.state.workspace_id)],
            options=[
                Option(
                    label=workspace.name,
                    action_id=add_action_id(
                        ActionIdTypes.select_workspace_on_convert_new_task_modal, workspace.id))
                for workspace in workspaces
            ],
        )

        project_text_paragraph = TextParagraph(content=get_translated_text(self.action_request.user_preferences.language, "viewtask.project"))
        projects: list[Project] = await project_service.get_all_projects_recursive(
            self.action_request, self.state.workspace_id)

        project_select = Select(
            placeholder=get_translated_text(self.action_request.user_preferences.language, "newtask.placeholder.project"),
            trigger_on_input=True,
            value=[''],
            options=[
                Option(
                    label=project.name,
                    action_id=add_action_id(ActionIdTypes.select_project_on_convert_new_task_modal, project.id))
                for project in projects
            ],
        )

        task_title_text_paragraph = TextParagraph(content=get_translated_text(self.action_request.user_preferences.language, "tasktitle.label"))
        task_title_input = Input(
            action_id='task_title_input',
            trigger_on_input=False,
            value=email_detail.subject
        )

        desc_text_paragraph = TextParagraph(content=get_translated_text(self.action_request.user_preferences.language, "task.description"))
        desc_textarea = Textarea(
            action_id='desc_textarea',
            height=SizeTypes.small,
            placeholder=get_translated_text(self.action_request.user_preferences.language, "describe.this.task")
        )

        close_button = Button(
            label=get_translated_text(self.action_request.user_preferences.language, "cancel.button"),
            style="primary",
            static_action=StaticAction(
                action_type="close_view"
            )
        )
        convert_button = Button(
            label=get_translated_text(self.action_request.user_preferences.language, "convert.button"),
            style="primary_filled",
            action_id=ActionIdTypes.convert_to_new_task,
            disabled=True
        )

        return View(
            view_id=self.view_id,
            state=self.state.to_bytes(),
            header=Header(
                title=get_translated_text(self.action_request.user_preferences.language, "converttask.title")

            ),
            body=Body(
                elements=[workspace_text_paragraph, workspace_select, project_text_paragraph,
                          project_select, task_title_text_paragraph, task_title_input,
                          desc_text_paragraph, desc_textarea]
            ),
            footer=Footer(buttons=[close_button, convert_button])
        )


class WorkspaceChangeDrawManager(ImapDrawManager):
    async def draw(self) -> SwitResponse:
        new_view = await self.build_view()

        return SwitResponse(
            callback_type=ViewCallbackType.update,
            new_view=new_view
        )

    async def build_view(self) -> View:
        current_view = self.action_request.current_view
        workspace_id = ActionIdTypes.get_action_value(current_view.body.elements[1].value[0])
        projects: list[Project] = await project_service.get_all_projects_recursive(
            self.action_request, workspace_id)
        current_view.body.elements[3] = Select(
            placeholder=get_translated_text(self.action_request.user_preferences.language, "newtask.placeholder.project"),
            trigger_on_input=True,
            value=[''],
            options=[
                Option(
                    label=project.name,
                    action_id=add_action_id(ActionIdTypes.select_project_on_convert_new_task_modal, project.id))
                for project in projects
            ],
        )
        return self.action_request.current_view


class ProjectChangeDrawManager(ImapDrawManager):
    async def draw(self) -> SwitResponse:
        assert self.action_request.current_view, "current_view check!!"
        new_view = await self.build_view()

        return SwitResponse(
            callback_type=ViewCallbackType.update,
            new_view=new_view
        )

    async def build_view(self) -> View:
        convert_button: Button = self.action_request.current_view.footer.buttons[1]
        convert_button.disabled = False
        return self.action_request.current_view


class ConvertCloseModalDrawManager(ImapDrawManager):
    async def draw(self) -> SwitResponse:
        assert self.state.workspace_id, "check workspace_id !!"
        assert self.state.email_detail_raw, "check email_detail_raw !!"
        current_view = self.action_request.current_view

        workspace_id = ActionIdTypes.get_action_value(current_view.body.elements[1].value[0])
        project_id: str = ActionIdTypes.get_action_value(current_view.body.elements[3].value[0])
        title: str = current_view.body.elements[5].value
        desc: str = current_view.body.elements[7].value

        await task_service.convert_to_new_task(
            action_request=self.action_request,
            workspace_id=workspace_id,
            project_id=project_id,
            mail_raw=self.state.email_detail_raw,
            title=title or self.action_request.current_view.body.elements[3].placeholder,
            desc=desc
        )
        return SwitResponse(
            callback_type=ViewCallbackType.close,
            new_view=self.action_request.current_view
        )

    async def build_view(self) -> View:
        pass
