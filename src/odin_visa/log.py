import logging

import structlog
from structlog.dev import ConsoleRenderer
from structlog.types import EventDict


def is_instrument_log(
    _logger: logging.Logger,
    _method_name: str,
    event_dict: EventDict,
) -> EventDict:
    if event_dict.get("_instrument") is True:
        raise structlog.DropEvent

    return event_dict


def configure_structlog(*, debug_traces: bool = False) -> None:
    renderer = ConsoleRenderer.get_active()
    renderer.level_styles = {
        **renderer.level_styles,
        "debug": "\x1b[90m",
    }

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f"),
    ]

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )

    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        handler.setFormatter(formatter)

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            *([is_instrument_log] if not debug_traces else []),
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
