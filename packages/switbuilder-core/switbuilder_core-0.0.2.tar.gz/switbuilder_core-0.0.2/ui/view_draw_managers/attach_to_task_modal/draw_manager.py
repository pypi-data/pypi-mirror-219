from action.constants import ActionIdTypes
from lokalise import get_translated_text
from project import service as project_service
from project.schemas import Project
from task import service as task_service
from task.schemas import Task
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
from workspace import service as workspace_service


class AttachTaskModalDrawManager(ImapDrawManager):
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
        workspace_text_paragraph = TextParagraph(
            content=get_translated_text(self.action_request.user_preferences.language, "workspace"))
        workspaces = await workspace_service.get_all_workspaces_recursive(
            self.action_request)
        workspace_select = Select(
            placeholder=get_translated_text(self.action_request.user_preferences.language, "link.placeholder"),
            trigger_on_input=True,
            value=[add_action_id(
                ActionIdTypes.select_workspace_on_attach_new_task_modal, self.state.workspace_id)],
            options=[
                Option(
                    label=workspace.name,
                    action_id=add_action_id(
                        ActionIdTypes.select_workspace_on_attach_new_task_modal, workspace.id))
                for workspace in workspaces
            ],
        )
        project_text_paragraph = TextParagraph(markdown=False, content="Project")

        projects: list[Project] = await project_service.get_all_projects_recursive(
            self.action_request, self.state.workspace_id)

        project_select = Select(
            placeholder=get_translated_text(
                self.action_request.user_preferences.language, "newtask.placeholder.project"),
            trigger_on_input=True,
            value=[''],
            options=[
                Option(
                    label=project.name,
                    action_id=add_action_id(ActionIdTypes.select_project_on_attach_task_modal, project.id))
                for project in projects
            ],
        )

        task_text_paragraph = TextParagraph(content=get_translated_text(
            self.action_request.user_preferences.language, "attachtotask.task.label"))
        task_select = Select(
            placeholder=get_translated_text(
                self.action_request.user_preferences.language, "select.task"),
            trigger_on_input=True,
            value=[''],
            options=[],
        )

        close_button = Button(
            label=get_translated_text(self.action_request.user_preferences.language, "cancel.button"),
            style="primary",
            static_action=StaticAction(
                action_type="close_view"
            )
        )
        attach_button = Button(
            label=get_translated_text(self.action_request.user_preferences.language, "attach.button"),
            style="primary_filled",
            action_id=ActionIdTypes.attach_to_task,
            disabled=True
        )

        return View(
            view_id=self.view_id,
            state=self.state.to_bytes(),
            header=Header(
                title=get_translated_text(self.action_request.user_preferences.language, "attachtotask.title")
            ),
            body=Body(
                elements=[workspace_text_paragraph, workspace_select, project_text_paragraph,
                          project_select, task_text_paragraph, task_select]
            ),
            footer=Footer(buttons=[close_button, attach_button])
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
            placeholder=get_translated_text(self.action_request.user_preferences.language, "link.placeholder"),
            trigger_on_input=True,
            value=[''],
            options=[
                Option(
                    label=project.name,
                    action_id=add_action_id(ActionIdTypes.select_project_on_attach_task_modal, project.id))
                for project in projects
            ],
        )

        current_view.body.elements[5] = Select(
            placeholder=get_translated_text(
                self.action_request.user_preferences.language, "select.task"),
            trigger_on_input=True,
            value=[''],
            options=[],
        )

        attach_button: Button = self.action_request.current_view.footer.buttons[1]
        attach_button.disabled = True

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
        current_view = self.action_request.current_view
        project_id: str = ActionIdTypes.get_action_value(current_view.body.elements[3].value[0])
        tasks: list[Task] = await task_service.get_tasks(
            action_request=self.action_request, project_id=project_id
        )

        task_select = Select(
            placeholder=get_translated_text(
                self.action_request.user_preferences.language, "select.task"),
            trigger_on_input=True,
            value=[''],
            options=[
                Option(
                    label=task.title,
                    action_id=add_action_id(ActionIdTypes.select_task_on_attach_task_modal, task.id))
                for task in tasks
            ],
        )

        current_view.body.elements[5] = task_select

        attach_button: Button = self.action_request.current_view.footer.buttons[1]
        attach_button.disabled = True

        return self.action_request.current_view


class TaskChangeDrawManager(ImapDrawManager):
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


class AttachCloseModalDrawManager(ImapDrawManager):
    async def draw(self) -> SwitResponse:
        assert self.state.workspace_id, "check workspace_id !!"
        assert self.state.email_detail_raw, "check email_detail_raw !!"

        # workspace_id = self.state.workspace_id
        # project_id: str = ActionIdTypes.get_action_value(self.action_request.current_view.body.elements[1].value[0])
        # title: str = self.action_request.current_view.body.elements[3].value
        #
        # await task_service.convert_to_new_task(
        #     action_request=self.action_request,
        #     workspace_id=workspace_id,
        #     project_id=project_id,
        #     mail_raw=self.state.email_detail_raw,
        #     title=title or self.action_request.current_view.body.elements[3].placeholder,
        # )

        current_view = self.action_request.current_view
        task_id: str = ActionIdTypes.get_action_value(current_view.body.elements[5].value[0])
        res = await task_service.attach_to_task(
            self.action_request, self.state.workspace_id, self.state.email_detail_raw, task_id)

        return SwitResponse(
            callback_type=ViewCallbackType.close,
            new_view=self.action_request.current_view
        )

    async def build_view(self) -> View:
        pass
