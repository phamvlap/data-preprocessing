from utils.constants import NoiseType, SpecialToken, TokenizerType


def get_config() -> dict:
    config = {
        "dataset_dir": "dataset",
        "tokenizer_dir": "dataset/tokenizer",
        "seed": 42,
        "max_sample": 10,
        "raw_data_path": "path/to/raw/data",
        "train_data_path": "path/to/trainr/data",
        "desc_path": "path/to/desc/file",
        "min_len_token": 6,
        "max_len_token": 196,
        "ranges": [(6, 100, 0.15), (101, 196, 0.15)],  # (min_len, max_len, ratio)
        "lang_src": "en",
        "lang_tgt": "cleaned_en",
        "vocab_size_src": 35000,
        "vocab_size_tgt": 35000,
        "tokenizer_type_src": TokenizerType.BPE,
        "tokenizer_type_tgt": TokenizerType.BPE,
        "min_freq": 2,
        "special_tokens": [
            SpecialToken.UNK,
            SpecialToken.PAD,
            SpecialToken.MASK,
        ],
        "is_train_tokenizer": True,
        "noise_types": [
            NoiseType.TOKEN_MASKING,
            NoiseType.DOCUMENT_ROTATION,
        ],
        "ratio": [0.15, None],
        "tokenizer_file": "tokenizer_{0}.json",
    }

    return config
