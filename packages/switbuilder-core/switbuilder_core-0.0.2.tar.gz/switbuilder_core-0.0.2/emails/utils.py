def get_convert_to_new_task_url() -> str:
    return f'v1/api/task.mail.create'


def get_attach_to_task_url() -> str:
    return f'v1/api/task.mail.append'


def get_share_to_dm_url() -> str:
    return f'v1/api/contents.mail.create'
