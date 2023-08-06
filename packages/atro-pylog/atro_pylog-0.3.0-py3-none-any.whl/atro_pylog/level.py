import logging


def str_to_level(level: str | int) -> int:
    if isinstance(level, int):
        return level
    match level.lower():
        case "debug":
            return logging.DEBUG
        case "info":
            return logging.INFO
        case "warning":
            return logging.WARNING
        case "error":
            return logging.ERROR
        case "critical":
            return logging.CRITICAL
        case _:
            raise Exception(f"Unknown logger level: {level}")


def level_to_str(level: str | int) -> str:
    if isinstance(level, str):
        if level.isdigit():
            level = int(level)
        else:
            return level
    match level:
        case logging.DEBUG:
            return "DEBUG"
        case logging.INFO:
            return "INFO"
        case logging.WARNING:
            return "WARNING"
        case logging.ERROR:
            return "ERROR"
        case logging.CRITICAL:
            return "CRITICAL"
        case _:
            raise Exception(f"Unknown logger level: {level}")
