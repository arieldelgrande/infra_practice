import os
from dotenv import load_dotenv
from src.config.staging import StagingSettings
from src.config.production import ProductionSettings
from src.config.development import DevSettings

load_dotenv()

env_value = os.environ.get("ENV")


match env_value:
    case "staging":
        settings = StagingSettings(
            env=env_value,
        )
    case "production":
        settings = ProductionSettings(
            env=env_value,
        )
    case _:
        settings = DevSettings(
            env=env_value,
        )
