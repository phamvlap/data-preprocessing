import re
import contractions


def split_text(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?]) +", text)
    return sentences


def split_text_by_length(text: str, min_len: int, max_len: int) -> list[str]:
    original_sentences = split_text(text)
    sentences = []
    for s in original_sentences:
        if len(s.split()) < max_len:
            sentences.append(s)

    chunks = []
    i = 0

    while i < len(sentences):
        chunk = [sentences[i]]
        chunk_length = len(sentences[i].split())
        j = i + 1
        i = j

        while j < len(sentences):
            if chunk_length + len(sentences[j].split()) <= max_len:
                chunk.append(sentences[j])
                chunk_length += len(sentences[j].split())
                j += 1
                i = j
            else:
                break

        if chunk_length >= min_len:
            chunks.append(" ".join(chunk))
    return chunks


def split_words(sentence: str) -> list[str]:
    words = re.findall(r"\b\w+\b", sentence)
    return words


def remove_urls(text: str) -> str:
    return re.sub(r"http[s]?:\/\/\S+|www\.\S+", "", text, flags=re.MULTILINE)


def remove_html_tags(text: str) -> str:
    return re.sub(r"<.*?>", "", text)


def normalize_punctuation(text: str) -> str:
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"([,.;!?\(\)\[\]\{\}])", r" \1 ", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def normalize_en_text(text: str) -> str:
    text = text.lower()
    text = contractions.fix(text)
    text = remove_urls(text)
    text = remove_html_tags(text)
    text = normalize_punctuation(text)
    return text
