import logging
from functools import wraps


def add_handler(logger: logging.Logger):
    if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '[swit-logger] %(asctime)s - (function)%(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)


def get_logger(func_name: str):
    logger = logging.getLogger(func_name)
    add_handler(logger)
    return logger


def logger_decorator():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            logger = logging.getLogger(f"{func.__name__}")
            add_handler(logger)
            return await func(*args, **kwargs, logger=logger)

        return wrapper

    return decorator
