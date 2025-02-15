# -*- coding: utf-8 -*-
# @Time    : 2024/7/11 17:51
# @Author  : JIAMID
# @Email   : jiamid@qq.com
# @File    : logger.py
# @Software: PyCharm
import logging
from pprint import pformat
import sys
from loguru import logger
import os


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentaion.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def format_record(record: dict) -> str:
    """
    Custom format for loguru loggers.
    Uses pformat for log any data like request/response body during debug.
    Works with logging if loguru handler it.
    Example:
    """
    format_string: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | " \
                         "<level>{level: <8}</level> | " \
                         "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"], indent=4, compact=True, width=88
        )
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"
    return format_string


def init_logging(file_name: str = 'bot_service'):
    intercept_handler = InterceptHandler()
    logging.root.setLevel(25)

    seen = set()
    for name in [
        *logging.root.manager.loggerDict.keys(),
        'gunicorn',
        'gunicorn.access',
        'gunicorn.error',
        'uvicorn',
        'uvicorn.access',
        'uvicorn.error',
    ]:
        if name not in seen:
            seen.add(name)
            cur_logger = logging.getLogger(name)
            cur_logger.propagate = False
            cur_logger.handlers = [intercept_handler]
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    log_dir = os.path.realpath(os.path.join(project_dir, 'logs'))
    logger.configure(handlers=[
        {'sink': sys.stdout,
         'level': 0,
         'format': format_record},
        {'sink': f'{log_dir}/info/{file_name}_info.log',
         'level': 25,
         'format': format_record,
         'enqueue': True,
         'rotation': '5MB',
         'retention': 15,
         'encoding': 'utf8'},
        {'sink': f'{log_dir}/error/{file_name}_error.log',
         'level': 'ERROR',
         'format': format_record,
         'enqueue': True,
         'rotation': '10MB',
         'retention': 15,
         'encoding': 'utf8'},
    ])
