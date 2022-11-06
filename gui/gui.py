import openai
import streamlit as st

from libs.parser import Parser


class Emojis:
    HAMMER = '\U0001F528'
    LIGHTNING = '\U000026A1'
    GEAR = '\U00002699'
    FEATHER = '\U0001FAB6'
    SLEEPING = '\U0001F4A4'
    BOOK = '\U0001F4D6'


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
        self.settings.API_KEY = st.sidebar.text_input('OpenAI API Key:', type='password')
        self.settings.MODEL = st.sidebar.selectbox(
            'GPT-3 model',
            ('text-davinci-002', 'text-curie-001', 'text-babbage-001', 'text-ada-001')
        )
        # self.settings.PROMPT
        self.settings.TEMPERATURE = st.sidebar.slider('Temperature', 0.0, 1.0, 0.7)
        self.settings.MAX_TOKENS = st.sidebar.slider('Maximum length', 1, 3857, 128)
        self.settings.TOP_P = st.sidebar.slider('Top P', 0.0, 1.0, 1.0)
        self.settings.FREQUENCY_PENALTY = st.sidebar.slider('Frequency penalty', 0.0, 2.0, 0.0)
        self.settings.PRESENCE_PENALTY = st.sidebar.slider('Presence penalty', 0.0, 2.0, 0.0)

        st.sidebar.title(f'Perfectly matched parameters')

        st.sidebar.code('Temperature: 1.0\nMaximum length: 128\nTop P: 1.0\nFrequency penalty: 0.0\nFrequency penalty: 0.0')

        st.sidebar.title(f'Parameters description')

        st.sidebar.subheader('GPT-3 model')
        st.sidebar.write('The model which will generate the completion. Some models are suitable for natural language tasks, others specialize in code.')

        st.sidebar.subheader('Temperature')
        st.sidebar.write('Controls randomness: Lowering results in less random completions. As the temperature approaches zero, the model will become deterministic and repetitive.')

        st.sidebar.subheader('Maximum length')
        st.sidebar.write('The maximum number of tokens to generate. Requests can use up to 2,048 or 4,000 tokens shared between prompt and completion. The exact limit varies by model. (One token is roughly 4 characters for normal English text)')

        st.sidebar.subheader('Top P')
        st.sidebar.write('Controls diversity via nucleus sampling: 0.5 means half of all likelihood-weighted options are considered.')

        st.sidebar.subheader('Frequency penalty')
        st.sidebar.write("How much to penalize new tokens based on their existing frequency in the text so far. Decreases the model's likelihood to repeat the same line verbatim.")

        st.sidebar.subheader('Presence penalty')
        st.sidebar.write("How much to penalize new tokens based on whether they appear in the text so far. Increases the model's likelihood to talk about new topics.")

    def setup_main_page(self) -> None:
        st.subheader(f'{self.emojis.SLEEPING} Bored with long texts, descriptions and so on? {self.emojis.SLEEPING}')
        st.subheader(f'{self.emojis.BOOK} Now you can read less while learning almost as much knowledge! {self.emojis.BOOK}')

        input_text = st.text_area(label='Enter the text to be summarized:')

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

        tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

        with tab1:
            st.header("A cat")
            st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

        with tab2:
            st.header("A dog")
            st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

        with tab3:
            st.header("An owl")
            st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
