from switcore.constants import Environment


def get_swit_openapi_base_url(env: Environment) -> str:
    if env == Environment.LOCAL or env == Environment.PROD:
        return "https://openapi.swit.io"
    elif env == Environment.EXPRESS:
        return 'https://openapi.swit.express'
    elif env == Environment.DEV:
        return 'https://openapi2.swit.dev'
    else:
        raise ValueError(f"Unknown env: {env}")
