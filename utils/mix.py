import torch
import random
import numpy as np
from pathlib import Path

from .constants import NoiseType
from .noises import (
    token_masking,
    token_deletion,
    text_infilling,
    sentence_permutation,
    document_rotation,
)


def set_seed(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def make_dir(dir_path: str) -> None:
    if not Path(dir_path).exists():
        Path(dir_path).mkdir(parents=True, exist_ok=True)


def write_file(file_path: str, content: str) -> None:
    dir_path = file_path.rsplit("/", 1)[0]
    make_dir(dir_path)
    with open(file_path, "w") as f:
        f.write(content)


def find_max_length(data: list[str]) -> int:
    max_length = 0
    for sent in data:
        max_length = max(max_length, len(sent.split()))
    return max_length


def get_noise_fn(noise_type: str) -> callable:
    noise_fns = {
        NoiseType.TOKEN_MASKING: token_masking,
        NoiseType.TOKEN_DELETION: token_deletion,
        NoiseType.TEXT_INFILLING: text_infilling,
        NoiseType.SENTENCE_PERMUTATION: sentence_permutation,
        NoiseType.DOCUMENT_ROTATION: document_rotation,
    }
    return noise_fns[noise_type]
