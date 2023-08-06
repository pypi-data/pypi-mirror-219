import logging
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseLoggerSettings(BaseSettings):
    name: str = "pylog"
    type: str = "rich"
    level: int | str = logging.DEBUG
    msg_format: str = "%(message)s"
    date_format: str = "%X"

    model_config = SettingsConfigDict(
        env_prefix="ATRO_PYLOG_",
        env_file=[(Path.home() / ".config" / "atro" / "pylog.env").as_posix(), ".env"],
        env_file_encoding="utf-8",
    )


class OpenTelemetryLoggerSettings(BaseLoggerSettings):
    service_name: str = "pylog"
    instance_id: str = "pylog"
    endpoint: str | None = None

    model_config = SettingsConfigDict(
        env_prefix="ATRO_PYLOG_OPENTELEMETRY",
        env_file=[(Path.home() / ".config" / "atro" / "pylog.env").as_posix(), ".env"],
        env_file_encoding="utf-8",
    )
