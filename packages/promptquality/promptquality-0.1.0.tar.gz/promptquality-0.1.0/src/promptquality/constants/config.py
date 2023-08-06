from enum import Enum


class ConfigDefaults(str, Enum):
    console_url = "https://console.cloud.rungalileo.io/"
    config_directory = ".galileo"
    config_filename = "pq-config.json"


class ConfigEnvironmentVariables(str, Enum):
    console_url = "GALILEO_CONSOLE_URL"
    username = "GALILEO_USERNAME"
    password = "GALILEO_PASSWORD"
