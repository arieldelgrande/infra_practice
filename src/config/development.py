from src.config.config import CommonSettings


class DevSettings(CommonSettings):
    debug_mode: bool = True
    database_url: str = "etc"
