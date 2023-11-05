# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
import openai
openai.api_type = "azure"
openai.api_key = "617447e973f0448fa9342c8c807bb496"
openai.api_base = "https://oh-ai-openai-scu.openai.azure.com/"
openai.api_version = "2023-05-15"
deployment_id = ''
prompt = "The food was delicious and the waiter"
completion = openai.Completion.create(deployment_id=deployment_id,
                                      prompt=prompt, stop=".", temperature=0)
chat_completion = openai.Completion.create(
  model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}]
  )
print(f"{prompt}{completion['choices'][0]['text']}.")



# # create a completion
# completion = openai.Completion.create(deployment_id="deployment-name", prompt="Hello world")
# # print the completion
# print(completion.choices[0].text)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
