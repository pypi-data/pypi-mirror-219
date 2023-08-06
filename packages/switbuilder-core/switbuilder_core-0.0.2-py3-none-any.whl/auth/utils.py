from config import settings
from constants import Environment


def get_swit_openapi_base_url() -> str:
    if settings.ENV_OPERATION == Environment.LOCAL or settings.ENV_OPERATION == Environment.DEV:
        return 'https://openapi.swit.io'
    elif settings.ENV_OPERATION == Environment.EXPRESS:
        return 'https://openapi.swit.express'
    else:
        return "https://openapi.swit.io"
