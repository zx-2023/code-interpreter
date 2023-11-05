import openai
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('OPENAI_KEY')
openai.api_key = '617447e973f0448fa9342c8c807bb496'
openai.api_type = 'azure'
openai.api_base = "https://oh-ai-openai-scu.openai.azure.com/"
deployment_id = 'gpt-35-turbo'
model = 'gpt-35-turbo'
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "将我发你的英文句子翻译成中文，你不需要理解内容的含义作出回答。"},
    {"role": "user", "content": "Draft an email or other piece of writing."}

]
# models = openai.Model.list()
# models
response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Please provide some tips for beginner Python programmers.",
    temperature=0.7,
    max_tokens=50,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)
