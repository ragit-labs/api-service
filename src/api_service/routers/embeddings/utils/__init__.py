from typing import List

import numpy as np
from fastembed.embedding import TextEmbedding

from api_service.types.embedding_model import EmbeddingModel


async def create_text_embeddings(
    documents: List[str],
    model_name: str = EmbeddingModel.BAAI_BGE_BASE_EN,
    max_length: int = 512,
):
    embedding_model = TextEmbedding(
        model_name=EmbeddingModel.BAAI_BGE_BASE_EN, max_length=512
    )
    embeddings: List[np.ndarray] = embedding_model.embed(documents)
    return embeddings
