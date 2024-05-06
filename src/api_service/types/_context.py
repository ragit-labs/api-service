from pydantic import BaseModel, Field


class TContext(BaseModel):
    id: str = Field(..., title="Context ID", description="Context's ID")
    name: str = Field(..., title="Name", description="Context's Name")
    description: Optional[str] = Field(
        ..., title="Description", description="Context's Description"
    )
    readable_id: str = Field(
        ..., title="Readable ID", description="Context's Readable ID"
    )
    project_id: str = Field(..., title="Project ID", description="Context's Project ID")
    owner_id: str = Field(..., title="Owner ID", description="Context's Owner ID")
    search_mode: str = Field(
        ..., title="Search Mode", description="Context's Search Mode"
    )
    retrieval_length: str = Field(
        ..., title="Retrieval Length", description="Context's Retrieval Length"
    )
    docs_to_retrieve: str = Field(
        ..., title="Docs To Retrieve", description="Context's Docs To Retrieve"
    )
    max_doc_length: str = Field(
        ..., title="Max Doc Length", description="Context's Max Doc Length"
    )
    doc_overlap_length: str = Field(
        ..., title="Doc Overlap Length", description="Context's Doc Overlap Length"
    )
    embedding_model: str = Field(
        ..., title="Embedding Model", description="Context's Embedding Model"
    )
    embedding_dimension: str = Field(
        ..., title="Embedding Dimension", description="Context's Embedding Dimension"
    )
    distance_metric: str = Field(
        ..., title="Distance Metric", description="Context's Distance Metric"
    )
    semantic_search: str = Field(
        ..., title="Semantic Search", description="Context's Semantic Search"
    )
    extra_metadata: str = Field(
        ..., title="Extra Metadata", description="Context's Extra Metadata"
    )
    last_refreshed_at: str = Field(
        ..., title="Last Refreshed At", description="Context's Last Refreshed At"
    )
    created_at: str = Field(..., title="Created At", description="Context's Created At")
