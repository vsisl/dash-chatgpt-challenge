"""
Utilities & other helper functions.
"""
import openai  # chat-gpt API

openai.api_key = open("openai_api_key.txt", "r").read().strip("\n")


def get_completion(prompt, model="gpt-3.5-turbo"):
    """Creates chatGPT response

    :param prompt: str
    :param model: str; optional, default: "gpt-3.5-turbo"
    :return: str: response
    """
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]
