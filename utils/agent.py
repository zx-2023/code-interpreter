# agent.py
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from langchain.agents.agent_types import AgentType
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

def create_agent(csv_file: str):
    """
    Create an agent that can access and use a large language model (LLM).

    Args:
        csv_file: the csv file to interact with.

    Returns:
        An LLM agent that can access and use the LLM.
    """

    # Create an OpenAI object.
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo',
                     openai_api_base=openai.api_base, deployment_id=deployment,
                     openai_api_key=openai.api_key)

    # Create a csv agent
    return create_csv_agent(llm, csv_file, temperature=0,
                            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                            early_stopping_method="generate",
                            verbose=True, handle_parsing_errors=True)
def query_agent(agent, query):
    """
    Query an agent and return the response as a string.
    """
    prompt = (
            """
                I want you to act as a machine learning engineer who is good at comprehensive
                data analysis. For the following query, provide step-by-step instructions for 
                building a model, demonstrating various techniques with visuals, and suggest 
                online resources for further study. Also please answer what kind of machine 
                learning algorithms should be used when facing towards a modeling question.

                If you do not know the answer, reply as follows:
                {"answer": "I do not know."}

                Please answer the question precisely.
                Query: 
                """
            + query
    )

    # Run the prompt through the agent.
    response = agent.run(prompt)

    # Convert the response to a string.
    return response.__str__()