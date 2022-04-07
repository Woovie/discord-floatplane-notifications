"""
Configuration loader for Floatplane Discord bot
"""
import configparser
import os
from dataclasses import dataclass, field
from typing import Union


@dataclass
class FloatplaneConfiguration:
    """
    a
    """
    api_endpoint: str = "https://youshouldchangethis.com"
    video_url: str = "https://youshouldchangethis.com"
    channel: str = "youshouldchangethis"
    limit: int = 20
    runner_frequency: int = 60


@dataclass
class DiscordConfiguration:
    """
    a
    """
    channel_id: int = 0
    token: str = "youshouldchangethis"


@dataclass
class Configuration:
    """
    a
    """
    config: Union[configparser.ConfigParser, dict]# TODO Rename or remove this?
    configuration_type: str = "env"
    discord: DiscordConfiguration = field(default_factory=DiscordConfiguration)
    floatplane: FloatplaneConfiguration = field(default_factory=FloatplaneConfiguration)

    def __post_init__(self):
        self._load_configuration()

    def _load_configuration(self):
        match self.configuration_type:
            case "env":
                self._load_environment_data()
            case "ini":
                self._load_ini_data()
            case "toml":
                self._load_toml_data()

    def _load_environment_data(self):
        pass

    def _load_ini_data(self):# TODO Instead we should be setting this data directly to the discord and floatplane variables of the class
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def _load_toml_data(self):
        pass

class ConfigurationLoad:
    """
    a
    """
    def __init__(self):
        self.config = {}
        self._determine_configuration()

    def _determine_configuration(self):
        env_vars = dict(os.environ)
        if len(env_vars) > 0:
            pass
