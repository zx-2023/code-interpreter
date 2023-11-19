# agent.py
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from langchain.agents.agent_types import AgentType
import openai

# Setting up the api key and other arguments
openai.api_type = "azure"
openai.api_base = "https://oh-ai-openai-scu.openai.azure.com/"
openai.api_version = "2023-05-15"
deployment = 'gpt-35-turbo'


def _handle_error(error) -> str:
    return str(error)[:50]


def create_agent(api_key: str, df: pd.DataFrame = None):
    """
    Create an agent that can access and use a large language model (LLM).

    Args:
        df: the data frame to be analyzed.
        api_key: input by the user.

    Returns:
        An LLM agent that can access and use the LLM.
    """

    llm = ChatOpenAI(
        temperature=0, model="gpt-3.5-turbo-0613", engine=deployment,
        openai_api_key=api_key, streaming=True
    )
    tools = [PythonAstREPLTool()]
    agent_obj = create_pandas_dataframe_agent(llm, df, verbose=True,
                                              early_stopping_method="generate",
                                              agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                                              tools=tools,
                                              handle_parsing_errors=_handle_error)

    return agent_obj
