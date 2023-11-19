import langchain
import streamlit as st
import openai
from langchain.callbacks import StreamlitCallbackHandler

import pandas as pd
import os
from utils.userguide import welcome_message
from utils.agent import create_agent

st.title("Chat with your data using GPT3.5")
langchain.debug = True
openai.api_type = "azure"
openai.api_base = "https://oh-ai-openai-scu.openai.azure.com/"
openai.api_version = "2023-05-15"
deployment = 'gpt-35-turbo'
API_KEY = st.sidebar.text_input(
    label="OpenAI API Key",
    type="password",
)

data_format = {
    "csv": pd.read_csv,
    "xls": pd.read_excel,
    "xlsx": pd.read_excel,
}


def clear_submit():
    """
    Clear the Submit Button State
    Returns:

    """
    st.session_state["submit"] = False


@st.cache_data(ttl="2h")
def data_loader(uploaded_file):
    try:
        ext = os.path.splitext(uploaded_file.name)[1][1:].lower()
    except ValueError as e:
        ext = uploaded_file.split(".")[-1]
        if not ext:
            raise e
    if ext in data_format:
        return data_format[ext](uploaded_file)
    else:
        st.error(f"Unsupported file format: {ext}")
        return None


uploaded_file = st.file_uploader(
    "Upload a Data file",
    type=list(data_format.keys()),
    help="A non-empty excel file can be analyzed by the assisatant",
    on_change=clear_submit,
)

if uploaded_file is None:
    st.warning(
        "Please upload a valid csv or excel")

if uploaded_file:
    df = data_loader(uploaded_file)
    if df is None:
        st.stop()
    if df is not None:
        st.write("Overview of your uploaded data:")
        st.dataframe(df.head())

welcome_message()

if "messages" not in st.session_state or st.sidebar.button("Clear conversation history"):
    st.session_state["messages"] = [{"role": "assistant",
                                     "content": "How can I help you with your data?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if query := st.chat_input(placeholder="Submit a query here"):
    prompt = (
            """
                I want you to act as a data analyst who is good at comprehensive
                data analysis and machine learning. For the following query, provide step-by-step instructions for 
                building a model, demonstrating various techniques with visuals, and suggest 
                online resources for further study. Also please answer what kind of machine 
                learning algorithms should be used when facing towards a modeling question.
                
                You will not only answer in natural language, but also generate and run Python code.
                When requested to generate code, always test it anf check if it works before producing the final answer.
                If you do not know the answer, reply as follows:
                {"answer": "I do not know."}
                
                Do not overthink the problem, try to answer it precisely.
                Query: 
                """
            + query
    )
    st.session_state.messages.append({"role": "user", "content": query})
    st.chat_message("user").write(query)

    if not API_KEY:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    pandas_df_agent = create_agent(api_key=API_KEY, df=df)
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        try:
            response = pandas_df_agent.run(st.session_state.messages, callbacks=[st_cb])
        except ValueError as e:
            response = str(e)
            if not response.startswith("Could not parse LLM output: `"):
                raise e
            response = response.removeprefix("Could not parse LLM output: `").removesuffix("`")
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
