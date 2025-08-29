from src.config.config import CommonSettings

class StagingSettings(CommonSettings):
    debug_mode: bool = False
    database_url: str = "etc"