from typing import List

import numpy as np
from fastembed.embedding import TextEmbedding

from ..types.embedding_model import EmbeddingModel


def create_text_embeddings(
    documents: List[str],
    max_length: int,
    model_name: str = EmbeddingModel.BAAI_BGE_BASE_EN,
):
    embedding_model = TextEmbedding(
        model_name=model_name,
        max_length=max_length,
        cache_dir=".embeddings_model_cache",
    )
    embeddings: List[np.ndarray] = embedding_model.embed(documents)
    return embeddings
