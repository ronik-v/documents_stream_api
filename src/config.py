from pydantic_settings import SettingsConfigDict, BaseSettings


class AppSettings(BaseSettings):
    """App settings from .env"""

    model_config = SettingsConfigDict(
        env_file="../.env",
        case_sensitive=False,
    )

    APP_NAME: str
    APP_HOST: str
    APP_PORT: int
    STATIC_PATH: str


settings = AppSettings()

