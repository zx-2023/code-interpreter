import sys
from random import randint
from ..interface import csv_chat

sys.path.append("..")


def test_math():
    # we'll generate random integers between this min and max in our math tests
    min_number = randint(1, 99)
    max_number = randint(1001, 9999)

    n1 = randint(min_number, max_number)
    n2 = randint(min_number, max_number)

    test_result = n1 + n2 * (n1 - n2)

    # credit to open-interpreter git repo
    test_math_query = f"""
    Please perform the calculation `{n1} + {n2} * ({n1} - {n2})` 
    then reply with just the answer, nothing else. No confirmation. 
    No explanation. No words. Do not use commas. Do not show your work. 
    Just return the result of the calculation. Do not introduce the 
    results with a phrase like \"The result of the calculation is...\" 
    or \"The answer is...\"

    Round to 2 decimal places.
    """.strip()

    messages = csv_chat(user_input=test_math_query)
    print(n1)
    print(n2)
    print(messages)
    assert str(round(test_result, 2)) in messages[-1]["message"]
