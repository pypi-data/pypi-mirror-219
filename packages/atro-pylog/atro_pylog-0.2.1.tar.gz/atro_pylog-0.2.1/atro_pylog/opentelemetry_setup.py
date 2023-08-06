from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

from atro_pylog.settings import OpenTelemetryLoggerSettings


def open_telemetry_logger_setup(level: int, settings: OpenTelemetryLoggerSettings):
    trace.set_tracer_provider(TracerProvider())
    logger_provider = LoggerProvider(  # type: ignore
        resource=Resource.create(
            {
                "service.name": settings.service_name,
                "service.instance.id": settings.instance_id,
            },
        ),
    )
    set_logger_provider(logger_provider)
    exporter = OTLPLogExporter(endpoint=settings.endpoint)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    return LoggingHandler(level=level, logger_provider=logger_provider)
