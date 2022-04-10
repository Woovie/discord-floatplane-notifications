"""
Configuration loader for Floatplane Discord bot

Supports three modes
- Environment variables
- config.ini
- config.toml
"""
import configparser
import os
from dataclasses import dataclass, field


@dataclass
class FloatplaneConfiguration:
    """
    Floatplane configuration class

    Holds 5 properties, nothing else
    """
    api_endpoint: str = "https://youshouldchangethis.com"
    video_url: str = "https://youshouldchangethis.com"
    channel: str = "youshouldchangethis"
    limit: int = 20
    runner_frequency: int = 60


@dataclass
class DiscordConfiguration:
    """
    Discord configuration class
    Holds 2 properties, nothing else
    """
    channel_id: int = 0
    token: str = "youshouldchangethis"


@dataclass
class Configuration:
    """
    Primary configuration class

    This contains logic to figure out which configuration type is being used and preparing it for
    usage
    """
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
        env_vars = os.environ
        self.floatplane.api_endpoint = env_vars['FP_API_ENDPOINT']
        self.floatplane.channel = env_vars['FP_CHANNEL']
        self.floatplane.video_url = env_vars['FP_VIDEO_URL']
        self.floatplane.limit = int(env_vars['FP_LIMIT'])
        self.floatplane.runner_frequency = env_vars['FP_RUNNER_FREQUENCY']
        self.discord.channel_id = int(env_vars['DISCORD_CHANNEL_ID'])
        self.discord.token = env_vars['DISCORD_TOKEN']

    def _load_ini_data(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.floatplane.api_endpoint = config['floatplane']['api_endpoint']
        self.floatplane.channel = config['floatplane']['channel']
        self.floatplane.video_url = config['floatplane']['video_url']
        self.floatplane.limit = int(config['floatplane']['limit'])
        self.floatplane.runner_frequency = config['floatplane']['runner_frequency']
        self.discord.channel_id = int(config['discord']['channel_id'])
        self.discord.token = config['discord']['token']

    def _load_toml_data(self):
        pass

class ConfigurationLoad:
    """
    a
    """
    def __init__(self):
        self.config = {}
        #self._determine_configuration()

    def _determine_configuration(self):
        env_vars = dict(os.environ)
        if len(env_vars) > 0:
            pass
