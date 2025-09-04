import os
from src.common.utils.observability.config import Config, Styles, setup_logging

# Environment-aware logger setup
env = os.getenv("ENVIRONMENT", "development").lower()
service_name = os.getenv("SERVICE_NAME", "publish")

logger_config = Config(
    name=service_name,
    log_level="INFO",
    environment=env,
    style=Styles.Json if env != "development" else Styles.Standard,
    format_str="%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(kv_pairs)s",
)


if env != "development":
    logger = setup_logging(logger_config)
else:
    logger = setup_logging(logger_config)
