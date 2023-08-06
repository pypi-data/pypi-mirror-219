#File: utils_openai.py
import tiktoken

tiktoken_adjust_factor = 1.8


encoding = tiktoken.get_encoding("cl100k_base")
#encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
encoding = tiktoken.encoding_for_model("gpt-4")


def count_tokens(text,factor=tiktoken_adjust_factor):
    """
    Count the number of tokens in the provided text.

    Args:
    text (str): The text for which to count the tokens.

    Returns:
    int: The number of tokens in the text.
    """
    tokens = encoding.encode(str(text))
    token_count = int(round(len(tokens) * factor))
    return token_count
