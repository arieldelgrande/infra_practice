from typing import Literal, Type
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource


class CommonSettings(BaseSettings):
    """
    Base settings for FastAPI application.
    """

    app_name: str = "My FastAPI Application"
    admin_email: str = "ariel.delgrande@meltwater.com"
    env: Literal["development", "staging", "production", "testing"] = "development"
    debug_mode: bool = False
    docs_url: str = "/"
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return env_settings, dotenv_settings, init_settings, file_secret_settings
