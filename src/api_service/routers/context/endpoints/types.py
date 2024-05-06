from typing import Optional, Union

from pydantic import BaseModel, Field
from ragit_db.enums import DocumentEmbeddingDistanceMetric, DocumentSearchMode

from ....types.embedding_model import EmbeddingModel


class CreateContextRequest(BaseModel):
    name: str = Field(..., title="Context name", description="Name of the context")
    description: Optional[str] = Field(
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
    file_id: str = Field(
        ..., title="File ID", description="ID of the file to add to the context"
    )


class DeleteFileRequest(BaseModel):
    file_id: str = Field(
        ..., title="File ID", description="ID of the file to add to the context"
    )


class SearchRequest(BaseModel):
    context_id: str = Field(
        ..., title="Context ID", description="ID of the context to search"
    )
    query: str = Field(..., title="Query", description="Query to search in the context")


class TContext(BaseModel):
    id: str = Field(..., title="Context ID", description="Context's ID")
    name: str = Field(..., title="Name", description="Context's Name")
    description: Optional[str] = Field(
        ..., title="Description", description="Context's Description"
    )
    readable_id: int = Field(
        ..., title="Readable ID", description="Context's Readable ID"
    )
    project_id: str = Field(..., title="Project ID", description="Context's Project ID")
    owner_id: str = Field(..., title="Owner ID", description="Context's Owner ID")
    search_mode: str = Field(
        ..., title="Search Mode", description="Context's Search Mode"
    )
    retrieval_length: int = Field(
        ..., title="Retrieval Length", description="Context's Retrieval Length"
    )
    docs_to_retrieve: int = Field(
        ..., title="Docs To Retrieve", description="Context's Docs To Retrieve"
    )
    max_doc_length: int = Field(
        ..., title="Max Doc Length", description="Context's Max Doc Length"
    )
    doc_overlap_length: int = Field(
        ..., title="Doc Overlap Length", description="Context's Doc Overlap Length"
    )
    embedding_model: str = Field(
        ..., title="Embedding Model", description="Context's Embedding Model"
    )
    embedding_dimension: int = Field(
        ..., title="Embedding Dimension", description="Context's Embedding Dimension"
    )
    distance_metric: str = Field(
        ..., title="Distance Metric", description="Context's Distance Metric"
    )
    semantic_search: bool = Field(
        ..., title="Semantic Search", description="Context's Semantic Search"
    )
    extra_metadata: dict = Field(
        ..., title="Extra Metadata", description="Context's Extra Metadata"
    )
    last_refreshed_at: str = Field(
        ..., title="Last Refreshed At", description="Context's Last Refreshed At"
    )
    created_at: str = Field(..., title="Created At", description="Context's Created At")


class TDocument(BaseModel):
    id: str = Field(..., title="Document ID", description="Document's ID")
    context_id: str = Field(
        ..., title="Context ID", description="Document's Context ID"
    )
    file_id: str = Field(..., title="File ID", description="Document's File ID")
    document: str = Field(..., title="Document", description="Document's Document")
    file_name: str = Field(..., title="File Name", description="Document's File Name")
    file_type: str = Field(..., title="File Type", description="Document's File Type")
