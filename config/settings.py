"""This file is responsible for storing basic settings / configuration."""


class Settings:  # pylint: disable=too-few-public-methods
    """This class is responsible for storing basic settings / configuration."""

    API_KEY = None

    MODEL = 'text-davinci-002'

    TEMPERATURE = 0.7

    MAX_TOKENS = 128

    TOP_P = 1

    FREQUENCY_PENALTY = 0

    PRESENCE_PENALTY = 0
