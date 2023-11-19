import streamlit as st
import time


def welcome_message():
    """
    display sample queries
    """
    question_list = [
        'How many rows are there?',
        'How many rows have the first column value greater than 4.5?']
    st.write('I am a code interpreter, who are able to perform sophisticated'
             ' data analysis, write code and even make some interesting '
             'plots. Try submit a query as below:')
    st.write(question_list[0])
    st.write(question_list[1])
    time.sleep(1)