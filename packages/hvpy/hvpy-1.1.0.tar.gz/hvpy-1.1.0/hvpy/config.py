from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["LiveSettings", "set_api_url", "get_api_url"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="HELIOVIEWER_")
    api_url: str = Field("https://api.helioviewer.org/v2/")


def get_api_url() -> str:
    """
    Returns the API URL.
    """
    from hvpy.config import LiveSettings

    return LiveSettings.api_url


def set_api_url(url: str) -> None:
    """
    Sets the API URL.

    Parameters
    ----------
    url : str
        Base API URL.
    """
    from hvpy.config import LiveSettings

    LiveSettings.api_url = url


LiveSettings = Settings()
