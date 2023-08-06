from typing import Optional

from promptquality.types.config import Config, set_config, set_console_url


def login(console_url: Optional[str] = None) -> Config:
    """Login to Galileo Environment.

    By default, this will login to Galileo Cloud but can be used to login to
    the enterprise version of Galileo by passing in the console URL for the
    environment."""
    set_console_url(console_url)
    config = set_config(console_url)
    config.login()
    return config
