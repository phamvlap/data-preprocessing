import re
from tokenizers import Tokenizer


def is_valid_token_length(
    tokenizer: Tokenizer,
    text: str,
    min_len: int,
    max_len: int,
) -> bool:
    tokens = tokenizer.encode(text).ids
    return len(tokens) >= min_len and len(tokens) <= max_len


def is_string(text: str) -> bool:
    if any(char.isdigit() for char in text):
        return False
    return True


def is_valid_min_max_length(text: str, min_len: int, max_len: int) -> bool:
    return len(text.split()) >= min_len and len(text.split()) <= max_len


def is_exist_url(text: str) -> bool:
    url_compile = re.compile(r"http[s]?:\/\/\S+|www\.\S+")
    return bool(url_compile.search(text))
