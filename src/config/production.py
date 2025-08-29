from src.config.config import CommonSettings

class ProductionSettings(CommonSettings):
    debug_mode = False
    database_url = "etc"