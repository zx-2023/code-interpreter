## to be updated

interface.py is the main function of the interpreter, it generates responses to the query input by the end user.
Currently, it supports some comprehensive data analysis and plotting functions, and can do some elementary machine learning project with a proper query.  

To start with the program, user "pip install requirements.txt -r" first, then type in "streamlit run interface.py" from the command prompt  

To properly use the demo, make sure you have created a file named <secrets.toml>   
which has "OPEN_API_KEY=***" in it(*** stands for your openai api key), otherwise you'll have to create an environment variable  

Feel free to try questions such as:  
query = "who is Albert Einstein?"
query = "build a predictive model for this data, the label is given as the species"  
query = "show me the size of the data"  
query = "show me the range of the third column"  
query = "write python code with a deep learning model for the species"
