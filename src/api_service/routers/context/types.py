from typing import Optional, Union

from ragit_db.enums import DocumentEmbeddingDistanceMetric, DocumentSearchMode
from pydantic import BaseModel, Field

from ...types.embedding_model import EmbeddingModel


class CreateContextRequest(BaseModel):
    name: str = Field(..., title="Context name", description="Name of the context")
    description: str = Field(
        None, title="Context description", description="Description of the context"
    )
    project_id: str = Field(
        ...,
        title="Project ID",
        description="ID of the project to which the context belongs",
    )
    owner_id: str = Field(
        ..., title="Owner ID", description="ID of the owner of the context"
    )
    search_mode: DocumentSearchMode = Field(
        DocumentSearchMode.SEARCH_WITH_CITATIONS,
        title="Search mode",
        description="Search mode of the context",
    )
    retrieval_length: int = Field(
        1024, title="Retrieval length", description="Retrieval length of the context"
    )
    docs_to_retrieve: int = Field(
        10, title="Docs to retrieve", description="Number of documents to retrieve"
    )
    max_doc_length: int = Field(
        256, title="Max doc length", description="Maximum document length"
    )
    doc_overlap_length: int = Field(
        64, title="Doc overlap length", description="Document overlap length"
    )
    embedding_model: EmbeddingModel = Field(
        EmbeddingModel.BAAI_BGE_BASE_EN,
        title="Embedding model",
        description="Embedding model of the context",
    )
    embedding_dimension: int = Field(
        768,
        title="Embedding dimension",
        description="Embedding dimension of the context",
    )
    distance_metric: DocumentEmbeddingDistanceMetric = Field(
        DocumentEmbeddingDistanceMetric.COSINE,
        title="Distance metric",
        description="Distance metric of the context",
    )
    extra_metadata: Optional[dict] = Field(
        None, title="Extra metadata", description="Extra metadata for the context"
    )


class ProjectsContextRequest(BaseModel):
    project_id: str = Field(
        ...,
        title="Project ID",
        description="ID of the project to which the context belongs",
    )
    limit: int = Field(
        10, title="Limit", description="Limit of the number of contexts to return"
    )
    offset: int = Field(
        0, title="Offset", description="Offset of the contexts to return"
    )


class ContextRequest(BaseModel):
    context_id: str = Field(
        ..., title="Context ID", description="ID of the context to get"
    )


class GetContextsRequest(BaseModel):
    where: Union[ProjectsContextRequest, ContextRequest] = Field(
        ..., title="Context request", description="Request to get contexts"
    )


class AddFileRequest(BaseModel):
    context_id: str = Field(
        ...,
        title="Context ID",
        description="ID of the context to which the file belongs",
    )
    file_id: str = Field(
        ..., title="File ID", description="ID of the file to add to the context"
    )


class SearchRequest(BaseModel):
    context_id: str = Field(
        ..., title="Context ID", description="ID of the context to search"
    )
    query: str = Field(..., title="Query", description="Query to search in the context")