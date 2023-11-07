# agent.py
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
import pandas as pd
import streamlit as st
import openai

# Setting up the api key and other arguments
openai.api_key = st.secrets["OPEN_API_KEY"]
openai.api_type = "azure"
openai.api_base = "https://oh-ai-openai-scu.openai.azure.com/"
openai.api_version = "2023-05-15"
deployment = 'gpt-35-turbo'

def _handle_error(error) -> str:
    return str(error)[:50]

def create_agent(df: pd.DataFrame):
    """
    Create an agent that can access and use a large language model (LLM).

    Args:
        df: the dataframe handled by file uploader.

    Returns:
        An LLM agent that can access and use the LLM.
    """

    # Create an OpenAI object.
    llm = ChatOpenAI(temperature=0.0, model_name='gpt-3.5-turbo',
                     openai_api_base=openai.api_base, deployment_id=deployment,
                     openai_api_key=openai.api_key)

    # Create a Pandas DataFrame agent.
    return create_pandas_dataframe_agent(llm, df, verbose=False,
                                         handle_parsing_errors=_handle_error)

def query_agent(agent, query):
    """
    Query an agent and return the response as a string.
    Credit to a blog
    """

    prompt = (
        """
            For the following query, if it requires drawing a table, reply as follows:
            {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], 
            [value1, value2, ...], ...]}}

            If the query requires creating a bar chart, reply as follows:
            {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

            If the query requires creating a line chart, reply as follows:
            {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

            If the query requires cleaning the data, reply as follows:
            {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

            If you do not know the answer, reply as follows:
            {"answer": "I do not know."}

            Please think step by step.

            Below is the query.
            Query: 
            """
        + query
    )

    # Run the prompt through the agent.
    response = agent.run(prompt)

    # Convert the response to a string.
    return response.__str__()