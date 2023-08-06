import logging
import sys
from pathlib import Path

import stackprinter

sys.path.append(Path(__file__).resolve().parent.parent.as_posix())

from atro_pylog.level import level_to_str, str_to_level  # noqa E402
from atro_pylog.logger_type import LoggerType  # noqa E402
from atro_pylog.logger_type import str_to_logger_type  # noqa E402
from atro_pylog.opentelemetry_setup import open_telemetry_logger_setup  # noqa E402
from atro_pylog.rich_setup import rich_handler  # noqa E402
from atro_pylog.settings import LoggerSettings  # noqa E402

logger = logging.getLogger(__name__)


def exception_handler(exc_type, exc_value, exc_traceback):
    logger.critical(stackprinter.format(exc_value))


def set_logger(settings: LoggerSettings = LoggerSettings()):
    sys.excepthook = exception_handler
    handlers = []

    types = [str_to_logger_type(type.strip()) for type in settings.type.split(";")]
    for tp in types:
        match tp:
            case LoggerType.RICH:
                handlers.append(rich_handler(str_to_level(settings.level)))
            case LoggerType.OPENTELEMETRY:
                handlers.append(open_telemetry_logger_setup(str_to_level(settings.level), settings.otel_service_name, settings.otel_instance_id, settings.otel_endpoint))
            case _:
                raise Exception(f"Unknown logger type: {tp}")
    logger = logging.getLogger(settings.name)
    if logger.hasHandlers():
        logger.handlers.clear()

    logging.basicConfig(level=level_to_str(settings.level), format=settings.msg_format, datefmt=settings.date_format, handlers=handlers)

    return logger
