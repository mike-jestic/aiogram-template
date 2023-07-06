from typing import Union, List

from pydantic import Field

from ..config_model import ConfigModel


class BotConfig(ConfigModel):
    __filenames__ = ("config_dev.json", "config.json")

    bot_token: str = Field()
    database_uri: str = Field()
