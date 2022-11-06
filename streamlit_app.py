"""Runner file for Fake News Generator app."""

import openai
import streamlit as st


class Settings:
    API_KEY = None
    MODEL = 'text-davinci-002'
    PROMPT = ''
    TEMPERATURE = 0.7
    MAX_TOKENS = 128
    TOP_P = 1
    FREQUENCY_PENALTY = 0
    PRESENCE_PENALTY = 0


def validate_string_start(string: str) -> str:
    while True:
        if string[0].isalnum():
            break
        else:
            string = string[1:]
    return string


def main():
    """Standard main function."""

    st.title('🔨⚡ AbstracThor \U000026A1\U0001F528')

    st.sidebar.title('Settings')
    openai.api_key = st.sidebar.text_input('OpenAI API Key:', type='password')

    st.subheader(
        'Bored with long texts, descriptions and so on? Now you can read less while learning almost as much knowledge!'
    )

    input_text = st.text_area(
        label='Enter the text to be summarized:'
    )

    if openai.api_key:
        st.subheader('Shorter version of your text:')
        with st.spinner('Smithing your abstract... ⚡🔨'):
            response = openai.Completion.create(
                model='text-davinci-002',
                prompt=f'{input_text}\n\nTl;dr',
                temperature=0.7,
                max_tokens=128,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            output = response['choices'][0]['text']
            output = validate_string_start(string=output)
            st.write(output)


if __name__ == '__main__':
    main()
