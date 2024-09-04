import random
import numpy as np

from .constants import SpecialToken


def random_positions(seq_length: int, ratio: float = 0.15) -> list[int]:
    num_tokens = int(seq_length * ratio)
    return random.sample(range(1, seq_length), k=num_tokens)


def token_masking(text: str, ratio: float = 0.15) -> str:
    words = text.split()
    seq_length = len(words)
    num_masked_tokens = int(seq_length * ratio)

    masked_seq = [True] * num_masked_tokens + [False] * (seq_length - num_masked_tokens)
    random.shuffle(masked_seq)

    for i in range(seq_length):
        if masked_seq[i]:
            words[i] = SpecialToken.MASK

    return " ".join(words).strip()


def token_deletion(text: str, ratio: float = 0.15) -> str:
    words = text.split()
    seq_length = len(words)

    masked_positions = random_positions(seq_length=seq_length, ratio=ratio)

    unremoved_words = words.copy()
    for i in masked_positions:
        unremoved_words = unremoved_words[:i] + unremoved_words[i + 1 :]

    return " ".join(unremoved_words).strip()


def sentence_permutation(text: str, ratio: float = 0.15) -> str:
    sentences = text.split(".")

    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    random.shuffle(sentences)

    return " ".join(sentences).strip()


def document_rotation(text: str, ratio: float = None) -> str:
    words = text.split()
    pos = random.randint(0, len(words) - 1)

    rotated_words = words[pos:] + words[:pos]

    return " ".join(rotated_words).strip()


def min_random_position(left: int, right: int, num_iters: int) -> int:
    min_pos = right
    for _ in range(num_iters):
        pos = random.randint(left, right)
        min_pos = min(min_pos, pos)
    return min_pos


def text_infilling(text: str, lambd: int = 3, ratio: float = 0.15) -> str:
    words = text.split()
    seq_length = len(words)
    masked_text_spans_length = max(1, int(seq_length * ratio))

    masked_positions = []
    cur_pos = 0
    cur_text_spans_length = 0
    masked_words = words.copy()

    while (
        cur_pos < seq_length
        and cur_text_spans_length <= masked_text_spans_length
        and (masked_text_spans_length - cur_text_spans_length) < seq_length
    ):
        text_span_length = min(
            seq_length - cur_pos, max(1, int(np.random.poisson(lambd)))
        )
        if text_span_length == 0:
            masked_words = (
                masked_words[:cur_pos] + [SpecialToken.MASK] + masked_words[cur_pos:]
            )
            seq_length += 1
            cur_text_spans_length += 1
            cur_pos += 2
            continue

        if cur_pos > seq_length - (
            masked_text_spans_length - cur_text_spans_length + text_span_length
        ):
            break

        start = min_random_position(
            left=cur_pos + 1,
            right=seq_length
            - (masked_text_spans_length - cur_text_spans_length + text_span_length),
            num_iters=10,
        )
        end = start + text_span_length
        if end > seq_length:
            break

        masked_positions.append((start, end))
        cur_text_spans_length += text_span_length
        cur_pos = masked_positions[-1][1]

    for start, end in masked_positions:
        if start >= end:
            continue
        masked_words = masked_words[:start] + [SpecialToken.MASK] + masked_words[end:]

    return " ".join(masked_words).strip()
