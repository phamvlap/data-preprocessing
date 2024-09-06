class NoiseType:
    TOKEN_MASKING = "token_masking"
    TOKEN_DELETION = "token_deletion"
    TEXT_INFILLING = "text_infilling"
    SENTENCE_PERMUTATION = "sentence_permutation"
    DOCUMENT_ROTATION = "document_rotation"


class SpecialToken:
    MASK = "<mask>"
    UNK = "<unk>"
    PAD = "<pad>"


class TokenizerType:
    WORD_LEVEL = "wordlevel"
    BPE = "bpe"
    WORD_PIECE = "wordpiece"
