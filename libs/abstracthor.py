"""This file stores the Abstracthor class and all its methods."""

import openai

from config.settings import Settings
from libs.parser import Parser


class Abstracthor:
    """This class contains methods that use and execute the main OpenAI functionality."""

    TOO_LONG_DID_NOT_READ = 'Tl;dr'

    def __init__(self, settings: Settings):
        """
        Standard Abstracthor class constructor.

        :param Settings settings: basic settings
        """

        self.settings = settings

    def assign_api_key(self) -> None:
        """Assigns the OpenAI API key (regardless of its value)."""

        openai.api_key = self.settings.API_KEY

    def check_api_key(self) -> bool:
        """
        Checks the OpenAI API key.

        :return: True if the API key is not None, False if the API key is None (None should be default)
        """

        if openai.api_key:
            return True

        return False

    def process(self, input_text: str) -> str:
        """
        Uses the openai.Completion.create() method to generate an abstracted version of the passed text.

        :param str input_text: text to process
        :return: abstracted version of the passed text
        """

        output = openai.Completion.create(
            model=self.settings.MODEL,
            prompt=f'{input_text}\n\n{self.TOO_LONG_DID_NOT_READ}',
            temperature=self.settings.TEMPERATURE,
            max_tokens=self.settings.MAX_TOKENS,
            top_p=self.settings.TOP_P,
            frequency_penalty=self.settings.FREQUENCY_PENALTY,
            presence_penalty=self.settings.PRESENCE_PENALTY
        )['choices'][0]['text']

        return Parser.validate_string_start(string=output)
