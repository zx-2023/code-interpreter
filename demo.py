# Import Libraries

import openai
import streamlit as st
from streamlit_chat import message

# Open API key is saved in .streamlit file
openai.api_key = st.secrets["OPEN_API_KEY"]
# Generating responses from the api
openai.api_type = "azure"
openai.api_base = "https://oh-ai-openai-scu.openai.azure.com/"
openai.api_version = "2023-05-15"

deployment_id = 'gpt-35-turbo'
prompt = "Write code in Python 3 to implement the input"
# completion = openai.Completion.create(deployment_id=deployment_id,
#                                       prompt=prompt, stop=".", temperature=0)
#
# print(f"{prompt}{completion['choices'][0]['text']}.")
def generate_response(prompt):
    completions = openai.Completion.create(
        prompt=prompt,
        max_tokens=2048,
        deployment_id=deployment_id,
        stop=".",
        temperature=0.2
    )
    messages = completions.choices[0].text
    for choice in completions['choices']:
        print(choice['text'])
    return messages

# Creating the chatbot interfaces

st.title("Chatbot Powered By GPT3.5")

# Storing the input

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

# Creating a function that returns the user's input from a text input field

def get_text():
    input_text = st.text_input("I am a personal assistant, how can I help you?: ", key="input")
    return input_text

# We will generate response using the 'generate response' function and store into variable called output

user_input = get_text()

if user_input:
    output = generate_response(user_input)

    # Store the output
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)


# Finally we display the chat history

if st.session_state['generated']:

    for i in range(len(st.session_state['generated']) -1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')