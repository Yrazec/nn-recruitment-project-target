import openai

from config.settings import Settings
from libs.parser import Parser


class Abstracthor:

    TOOLONG_DID_NOT_READ = 'Tl;dr'

    def __init__(self, settings: Settings):
        self.settings = settings

    def assign_api_key(self) -> None:
        openai.api_key = self.settings.API_KEY

    def check_api_key(self) -> bool:
        if openai.api_key:
            return True
        return False

    def process(self, input_text: str) -> str:
        output = openai.Completion.create(
            model=self.settings.MODEL,
            prompt=f'{input_text}\n\n{self.TOOLONG_DID_NOT_READ}',
            temperature=self.settings.TEMPERATURE,
            max_tokens=self.settings.MAX_TOKENS,
            top_p=self.settings.TOP_P,
            frequency_penalty=self.settings.FREQUENCY_PENALTY,
            presence_penalty=self.settings.PRESENCE_PENALTY
        )['choices'][0]['text']
        return Parser.validate_string_start(string=output)
