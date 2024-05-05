from enum import Enum, unique


@unique
class EmbeddingModel(str, Enum):
    BAAI_BGE_BASE_EN = "BAAI/bge-base-en"
