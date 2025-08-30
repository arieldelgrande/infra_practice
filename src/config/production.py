from src.config.config import CommonSettings


class ProductionSettings(CommonSettings):
    debug_mode: bool = False
    database_url: str = "etc"
