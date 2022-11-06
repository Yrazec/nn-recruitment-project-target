import openai
import streamlit as st

from libs.parser import Parser


class Emojis:
    HAMMER = '\U0001F528'
    LIGHTNING = '\U000026A1'
    GEAR = '\U00002699'
    NUMERALS_ONE = '\U00000031'
    NUMERALS_TWO = '\U00000032'
    NUMERALS_THREE = '\U00000033'
    NUMERALS_FOUR = '\U00000034'
    NUMERALS_FIVE = '\U00000035'
    NUMERALS_SIX = '\U00000036'
    NUMERALS_SEVEN = '\U00000037'
    NUMERALS_EIGHT = '\U00000038'
    NUMERALS_NINE = '\U00000039'


class Settings:
    API_KEY = None
    MODEL = 'text-davinci-002'
    # PROMPT = ''
    TEMPERATURE = 0.7
    MAX_TOKENS = 128
    TOP_P = 1
    FREQUENCY_PENALTY = 0
    PRESENCE_PENALTY = 0


class MainGUI:
    def __init__(self):
        self.emojis = Emojis()
        self.settings = Settings()

        self.setup_title()
        self.setup_sidebar()
        self.setup_main_page()

    def setup_title(self) -> None:
        st.title(f'{self.emojis.HAMMER}{self.emojis.LIGHTNING} ABSTRACTHOR {self.emojis.LIGHTNING}{self.emojis.HAMMER}')

    def setup_sidebar(self) -> None:
        st.sidebar.title(f'{self.emojis.GEAR} SETTINGS {self.emojis.GEAR}')
        self.settings.API_KEY = st.sidebar.text_input(f'{self.emojis.NUMERALS_ONE} OpenAI API Key:', type='password')
        self.settings.MODEL = st.sidebar.selectbox(
            f'{self.emojis.NUMERALS_TWO} GPT-3 model',
            ('text-davinci-002', 'text-curie-001', 'text-babbage-001', 'text-ada-001')
        )
        # self.settings.PROMPT
        self.settings.TEMPERATURE = st.sidebar.slider('Temperature', 0.0, 1.0, 0.7)
        self.settings.MAX_TOKENS = st.sidebar.slider('Maximum length', 1, 3857, 128)
        self.settings.TOP_P = st.sidebar.slider('Top P', 0.0, 1.0, 1.0)
        self.settings.FREQUENCY_PENALTY = st.sidebar.slider('Frequency penalty', 0.0, 2.0, 0.0)
        self.settings.PRESENCE_PENALTY = st.sidebar.slider('Presence penalty', 0.0, 2.0, 0.0)

    def setup_main_page(self) -> None:
        st.subheader(' '.join([
            'Bored with long texts, descriptions and so on? Now you can',
            'read less while learning almost as much knowledge!'
        ]))

        input_text = st.text_area(
            label='Enter the text to be summarized:'
        )

        openai.api_key = self.settings.API_KEY

        if openai.api_key:
            st.subheader('Shorter version of your text:')
            with st.spinner('Forging your abstract... ⚡🔨'):
                response = openai.Completion.create(
                    model=self.settings.MODEL,
                    prompt=f'{input_text}\n\nTl;dr',
                    temperature=self.settings.TEMPERATURE,
                    max_tokens=self.settings.MAX_TOKENS,
                    top_p=self.settings.TOP_P,
                    frequency_penalty=self.settings.FREQUENCY_PENALTY,
                    presence_penalty=self.settings.PRESENCE_PENALTY
                )
                output = response['choices'][0]['text']
                output = Parser.validate_string_start(string=output)
                st.write(output)
