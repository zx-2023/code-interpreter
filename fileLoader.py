from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
import streamlit as st
import tempfile
from langchain.vectorstores import FAISS
import pandas as pd
from streamlit_chat import message
import openai
from agent import create_agent, query_agent
from interface import decode_response, write_response
import agent

st.title("Chat with your CSV using GPT3.5")
uploaded_file = st.sidebar.file_uploader("Please upload your CSV file", type="csv")

if uploaded_file:
    data = uploaded_file
if data is None:
    st.text_input("Please upload a csv file from the side bar.")
    raise TypeError("No valid file is uploaded")
   #pass filepath to CSVLoader
    # with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
    #     tmp_file.write(uploaded_file.getvalue())
    #     tmp_file_path = tmp_file.name
    #
    # loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8")
    # data_list = loader.load()

with st.expander('Overview of your data:'):
    df = pd.read_csv(data, index_col=0)
    st.write(df.head(5))

openai.api_type = "azure"
openai.api_base = "https://oh-ai-openai-scu.openai.azure.com/"
openai.api_version = "2023-05-15"
deployment = 'gpt-35-turbo'

question_list = [
  'How many rows are there?',
  'What is the range of values for the first column greater than 3?',
  'How many rows have the first column value greater than 4.5?',
  'Other']
query_text = st.selectbox('Select an example query:', question_list, disabled=not uploaded_file)

# embeddings = OpenAIEmbeddings(deployment='text-embedding-ada-002',
#                               openai_api_key=agent.API_KEY,
#                               openai_api_version=openai.api_version,
#                               openai_api_base=openai.api_base,
#                               openai_api_type=openai.api_type)
# vectorstore = FAISS.from_documents(data_list, embeddings)
# # remember chat history via conversational retrieval chain
# chain = ConversationalRetrievalChain.from_llm(
#     retriever=vectorstore.as_retriever())


# def conversational_chat(user_input):
#     result = chain({"question": user_input,
#                     "chat_history": st.session_state['history']})
#     st.session_state['history'].append((user_input, result["answer"]))
#
#     return result["answer"]

if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hello ! Ask me anything about " + uploaded_file.name + " 🤗"]

if 'past' not in st.session_state:
    st.session_state['past'] = ["Hey ! 👋"]

# container for the chat history
response_container = st.container()
# container for the user's text input
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_input("Ask a question about your csv data here:",
                                   placeholder="Submit query", key='input')
        submit_button = st.form_submit_button(label='Send')

    # if submit_button and user_input:
    #
    #     output = conversational_chat(user_input)
    #
    #     st.session_state['past'].append(user_input)
    #     st.session_state['generated'].append(output)

    if submit_button and user_input:

        # Create an agent from the CSV file.

        agent = create_agent(data)

        # Query the agent.
        if query_text is not 'Other':
            response = query_agent(agent=agent, query=query_text)

        if query_text is 'Other' and uploaded_file is not None:
            query_text = st.text_input('Enter your query:',
                                       placeholder='Enter query here ...', disabled=not uploaded_file)
            st.header('Output')
            response = query_agent(agent=agent, query=user_input)

        # Decode the response.
        decoded_response = decode_response(response)

        # Write the response to the Streamlit app.
        write_response(decoded_response)

if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")