from src.config.config import CommonSettings

class DevSettings(CommonSettings):
    debug_mode = True
    database_url = "etc"