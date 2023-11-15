import streamlit as st
import pandas as pd
import time
from utils.agent import create_agent, query_agent
from .utils.file_converter import convert_to_csv
from utils.response import decode_response, write_response
st.title("Chat with your CSV or XLSX using GPT3.5")


def file_uploader():
    uploaded_file = st.sidebar.file_uploader("Please upload a CSV/XLS/XLSX file "
                                             "with one sheet",
                                             type=["csv", 'xlsx', 'xls'],
                                             accept_multiple_files=False)

    data = uploaded_file
    if data is None:
        st.text_input("Please upload a csv file from the side bar.")
        raise TypeError("No valid file is uploaded")

    with st.expander('Overview of your data:'):
        if data.name[-3:] == 'csv':
            df = pd.read_csv(data)
        else:
            df = pd.read_excel(data)
        st.write(df.head(5))
    print(data)
    csv_file = convert_to_csv(data)
    print(csv_file)
    return csv_file


def user_guide():
    """
    display sample queries
    """
    question_list = [
        'How many rows are there?',
        'What is the range of values for the first column greater than 3?',
        'How many rows have the first column value greater than 4.5?']
    st.write('I am a code interpreter, who are able to perform sophisticated'
             ' data analysis, write code and even make some interesting '
             'plots. Try submit a query as below:')
    st.write(question_list[0])
    st.write(question_list[1])
    st.write(st.write(question_list[2]))
    st.divider()

    time.sleep(1)


def csv_chat(filename: str = None, user_input: str = None):
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    # container for the user's text input
    container = st.container()
    with container:
        with st.form(key='my_form', clear_on_submit=True):
            if user_input is None:
                user_input = st.text_input("Ask a question about your csv data here:",
                                           placeholder="Submit query", key='input')
                submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
                # Create an agent from the input file.

                agent = create_agent(csv_file=filename)

                # Query the agent.
                st.header('Output')
                response = query_agent(agent=agent, query=user_input)

                # Decode the response.
                decoded_response = decode_response(response)
                print(decoded_response)
                # Write the response to the Streamlit app.
                write_response(decoded_response)


if __name__ == "__main__":
    csv_file = file_uploader()
    user_guide()
    csv_chat(filename=csv_file)
