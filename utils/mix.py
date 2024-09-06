import torch
import random
import numpy as np


def set_seed(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def write_file(file_path: str, content: str) -> None:
    with open(file_path, "w") as f:
        f.write(content)


def find_max_length(data: list[str]) -> int:
    max_length = 0
    for sent in data:
        max_length = max(max_length, len(sent.split()))
    return max_length
