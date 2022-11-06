import openai
import pandas as pd
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

        st.sidebar.markdown('---')
        st.sidebar.title(f'Perfectly matched parameters')

        st.sidebar.code('Model: text-davinci-002\nTemperature: 1.0\nMaximum length: 128\nTop P: 1.0\nFrequency penalty: 0.0\nFrequency penalty: 0.0')

        st.sidebar.markdown('---')
        st.sidebar.title(f'Parameters description')

        st.sidebar.header('GPT-3 model')
        st.sidebar.write('The model which will generate the completion. Some models are suitable for natural language tasks, others specialize in code.')

        st.sidebar.header('Temperature')
        st.sidebar.write('Controls randomness: Lowering results in less random completions. As the temperature approaches zero, the model will become deterministic and repetitive.')

        st.sidebar.header('Maximum length')
        st.sidebar.write('The maximum number of tokens to generate. Requests can use up to 2,048 or 4,000 tokens shared between prompt and completion. The exact limit varies by model. (One token is roughly 4 characters for normal English text)')

        st.sidebar.header('Top P')
        st.sidebar.write('Controls diversity via nucleus sampling: 0.5 means half of all likelihood-weighted options are considered.')

        st.sidebar.header('Frequency penalty')
        st.sidebar.write("How much to penalize new tokens based on their existing frequency in the text so far. Decreases the model's likelihood to repeat the same line verbatim.")

        st.sidebar.header('Presence penalty')
        st.sidebar.write("How much to penalize new tokens based on whether they appear in the text so far. Increases the model's likelihood to talk about new topics.")

    def setup_main_page(self) -> None:

        main_page_tab, description_tab = st.tabs(["MAIN PAGE", "DESCRIPTION"])

        with main_page_tab:
            st.header(f'{self.emojis.SLEEPING} Bored with long texts, descriptions and so on? {self.emojis.SLEEPING}')
            st.header(f'{self.emojis.BOOK} Now you can read less while learning almost as much knowledge! {self.emojis.BOOK}')

            input_text = st.text_area(label='Enter the text to be summarized:')

            openai.api_key = self.settings.API_KEY

            if openai.api_key:
                st.header('Shorter version of your text:')
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

        with description_tab:
            st.write("OpenAI's GPT-3 models can understand and generate natural language. It offer four main models with different levels of power suitable for different tasks. Davinci is the most capable model, and Ada is the fastest.")
            df = pd.DataFrame(
                [
                    ['text-davinci-002', 'Most capable GPT-3 model. Can do any task the other models can do, often with less context. In addition to responding to prompts, also supports inserting completions within text.', '4,000 tokens', 'Up to Jun 2021'],
                    ['text-curie-001', 'Very capable, but faster and lower cost than Davinci.', '2,048 tokens', 'Up to Oct 2019'],
                    ['text-babbage-001', 'Capable of straightforward tasks, very fast, and lower cost.', '2,048 tokens', 'Up to Oct 2019'],
                    ['text-ada-001', 'Capable of very simple tasks, usually the fastest model in the GPT-3 series, and lowest cost.', '2,048 tokens', 'Up to Oct 2019']
                ],
                columns=('LATEST MODEL', 'DESCRIPTION', 'MAX REQUEST', 'TRAINING DATA')
            )
            hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
            st.markdown(hide_table_row_index, unsafe_allow_html=True)
            st.table(df)
            st.write('While Davinci is generally the most capable, the other models can perform certain tasks extremely well with significant speed or cost advantages. For example, Curie can perform many of the same tasks as Davinci, but faster and for 1/10th the cost.')
            st.write("It's recommend using Davinci while experimenting since it will yield the best results.")

            st.subheader('Davinci')
            st.write('Davinci is the most capable model family and can perform any task the other models can perform and often with less instruction. For applications requiring a lot of understanding of the content, like summarization for a specific audience and creative content generation, Davinci is going to produce the best results. These increased capabilities require more compute resources, so Davinci costs more per API call and is not as fast as the other models.')
            st.write('Another area where Davinci shines is in understanding the intent of text. Davinci is quite good at solving many kinds of logic problems and explaining the motives of characters. Davinci has been able to solve some of the most challenging AI problems involving cause and effect.')

            st.subheader('Curie')
            st.write('Curie is extremely powerful, yet very fast. While Davinci is stronger when it comes to analyzing complicated text, Curie is quite capable for many nuanced tasks like sentiment classification and summarization. Curie is also quite good at answering questions and performing Q&A and as a general service chatbot.')

            st.subheader('Babbage')
            st.write('Babbage can perform straightforward tasks like simple classification. It’s also quite capable when it comes to Semantic Search ranking how well documents match up with search queries.')

            st.subheader('Ada')
            st.write('Ada is usually the fastest model and can perform tasks like parsing text, address correction and certain kinds of classification tasks that don’t require too much nuance. Ada’s performance can often be improved by providing more context.')
