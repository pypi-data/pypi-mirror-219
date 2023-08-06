import base64
import logging

from action.schemas import ActionRequest
from imap.utils import decode_to_bytes_from_base64
from logger import logger_decorator
from task.schemas import Task
from task.utils import get_tasks_url, get_convert_to_new_task_url, get_attach_to_task_url


def get_task_or_null(tasks: list[Task], task_id: str) -> Task | None:
    ret = None
    for task in tasks:
        if task.id == task_id:
            ret = task
            break

    return ret


@logger_decorator()
async def get_tasks(
        action_request: ActionRequest,
        project_id: str,
        logger: logging.Logger
) -> list[Task]:
    params: dict = {
        "limit": 50,
        "project_id": project_id,
    }

    res = await action_request.swit_client.get(get_tasks_url(), params=params)

    data: dict = res.json()
    data = data.get('data', {})

    tasks_data: list[dict] = data.get('tasks', [])
    offset: str | None = data.get('offset', None)

    if res.status_code != 200:
        logger.error(f"get_tasks error: {res.json()}")

    if len(tasks_data) == 0:
        return []

    tasks = [Task(**task) for task in tasks_data]

    return tasks


@logger_decorator()
async def convert_to_new_task(
        action_request: ActionRequest,
        workspace_id: str,
        project_id: str,
        mail_raw: str,
        title: str,
        desc: str,
        logger: logging.Logger
):
    data = {
        "workspace_id": workspace_id,
        "project_id": project_id,
        "mail": base64.urlsafe_b64encode(decode_to_bytes_from_base64(mail_raw)).decode(),
        "title": title,
        "content": desc,
        # "step": "ToDo",
        "provider": "gmail",  # TODO to imap
    }

    # TODO step 을 설정 하는 화면 필요!
    # https://devdocs.swit.io/docs/core1/ref/operations/create-a-api-task-status-update
    # https://devdocs.swit.io/docs/core1/ref/operations/get-a-api-task-status-list
    res = await action_request.swit_client.post(get_convert_to_new_task_url(), json=data)
    if res.status_code != 200:
        logger.error(f"convert_to_new_task error: {res.json()}")


async def attach_to_task(
        action_request: ActionRequest,
        workspace_id: str,
        mail_raw: str,
        task_id: str,
):
    data = {
        "ws_id": workspace_id,
        "mail": base64.urlsafe_b64encode(decode_to_bytes_from_base64(mail_raw)).decode(),
        "log_id": task_id,
    }

    res = await action_request.swit_client.post(get_attach_to_task_url(), json=data)
    print(res.json())
