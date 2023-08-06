def get_tasks_url() -> str:
    return 'v1/api/task.list'


def get_convert_to_new_task_url() -> str:
    return f'v1/api/task.mail.create'  # TODO URL 변경


def get_attach_to_task_url() -> str:
    return f'v1/api/task.mail.append'
