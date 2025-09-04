import logging

from pythonjsonlogger import jsonlogger
from enum import Enum




class Styles(Enum):
    Json = "Json"
    Standard = "Standard"

class Config:
    def __init__(
        self,
        name: str="app",
        log_level="INFO",
        environment="development",
        format_str="%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(kv_pairs)s",
        style: Styles=Styles.Standard
    ):
        self.environment = environment
        self.log_level = log_level
        self.name = name
        self.format_str = format_str
        self.style = style

class DynamicLogger(logging.Logger):
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1, **kwargs):
        if extra is None:
            extra = {}
        if "kv_pairs" not in extra:
            extra["kv_pairs"] = {}
        if kwargs:
            extra["kv_pairs"].update(kwargs)
        super()._log(level, msg, args, exc_info=exc_info, extra=extra, stack_info=stack_info, stacklevel=stacklevel)

    def exception(self, msg, error_code=None, **kwargs):
        """Log an error with exception information, including optional error code."""
        extra = {"error_code": error_code} if error_code is not None else {}
        self.error(msg, exc_info=True, extra=extra, **kwargs)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if "kv_pairs" in record.__dict__:
            log_record.update(record.__dict__["kv_pairs"])
            del log_record["kv_pairs"]


def setup_logging(config: Config = Config()):
    formatter = logging.Formatter(config.format_str)
    if config.style == Styles.Json:
        formatter = CustomJsonFormatter()

    logging.setLoggerClass(DynamicLogger)

    # Basic logging setup
    _logger = logging.getLogger(config.name)
    _logger.setLevel(getattr(logging, config.log_level))
    _logger.handlers.clear()

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    _logger.addHandler(console_handler)

    return _logger

