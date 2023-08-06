from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable


class Settings(BaseSettings):
    """Settings for the LOTR API client."""

    BEARER_TOKEN: str

    class Config(BaseSettings.Config):
        """Settings configuration.

        Main purpose is to change the order of the settings sources to (in order): Init value,
        Environment variable, Secret File (secret) (not tested)

        Please see base class for more information
        Docs - https://docs.pydantic.dev/latest/usage/settings/#customise-settings-sources
        """

        @classmethod
        def customise_sources(  # noqa: D102
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            return env_settings, init_settings, file_secret_settings
