from __future__ import annotations

import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Integer, Boolean, PrimaryKeyConstraint, UniqueConstraint
from typing import List
from sqlalchemy.dialects.postgresql import  UUID, ENUM, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from ..enums import FileStatus, EmbeddingStatus, DocumentEmbeddingDistanceMetric, DocumentSearchMode, ContextPermission, ProjectPermission


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(), nullable=False)
    password: Mapped[str] = mapped_column(String(), nullable=False)
    first_name: Mapped[str] = mapped_column(String(), nullable=False)
    last_name: Mapped[str] = mapped_column(String(), nullable=False)
    signin_provider: Mapped[str] = mapped_column(String(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    __table_args__ = (UniqueConstraint("id", name="ux_user_id")),


class Project(Base):
    __tablename__ = "project"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    readable_id: Mapped[str] = mapped_column(String(), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    description: Mapped[str] = mapped_column(String(), nullable=True)

    __table_args__ = (UniqueConstraint("id", name="ux_project_id")),


class File(Base):
    __tablename__ = "file"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(), nullable=False)
    s3_key: Mapped[str] = mapped_column(String(), nullable=False)
    status: Mapped[FileStatus] = mapped_column(ENUM(FileStatus), nullable=False, default=FileStatus.PENDING)
    description: Mapped[str] = mapped_column(String(), nullable=True)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    __table_args__ = (UniqueConstraint("id", name="ux_file_id")),


class Context(Base):
    __tablename__ = "context"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(), nullable=False)
    description: Mapped[str] = mapped_column(String(), nullable=True)
    readable_id: Mapped[int] = mapped_column(Integer(), primary_key=True, nullable=False)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    search_mode: Mapped[DocumentSearchMode] = mapped_column(ENUM(DocumentSearchMode), nullable=False, default=DocumentSearchMode.SEARCH_WITH_CITATIONS)
    retrieval_length: Mapped[int] = mapped_column(Integer(), nullable=False, default=1024)
    docs_to_retrieve: Mapped[int] = mapped_column(Integer(), nullable=False, default=10)
    max_doc_length: Mapped[int] = mapped_column(Integer(), nullable=False, default=256)
    doc_overlap_length: Mapped[int] = mapped_column(Integer(), nullable=False, default=64)
    embedding_model: Mapped[str] = mapped_column(String(), nullable=False)
    embedding_dimension: Mapped[int] = mapped_column(Integer(), nullable=False, default=768)
    distance_metric: Mapped[DocumentEmbeddingDistanceMetric] = mapped_column(ENUM(DocumentEmbeddingDistanceMetric), nullable=False, default=DocumentEmbeddingDistanceMetric.COSINE)
    semantic_search: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
    extra_metadata: Mapped[dict] = mapped_column(JSONB(), nullable=True)
    last_refreshed_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)

    __table_args__ = (UniqueConstraint("id", name="ux_context_id")),


class UserProject(Base):
    __tablename__ = "user_project"
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("project.id"), primary_key=True)
    permission: Mapped[ProjectPermission] = mapped_column(ENUM(ProjectPermission), nullable=False, default=ProjectPermission.READ)


class UserContext(Base):
    __tablename__ = "user_context"
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True)
    context_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("context.id"), primary_key=True)
    permission: Mapped[ContextPermission] = mapped_column(ENUM(ContextPermission), nullable=False, default=ContextPermission.READ)


class UserFile(Base):
    __tablename__ = "user_file"
    file_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("file.id"), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True)


class ContextFile(Base):
    __tablename__ = "context_file"
    file_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("file.id"), primary_key=True)
    context_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("context.id"), primary_key=True)
    linked_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    status: Mapped[EmbeddingStatus] = mapped_column(ENUM(EmbeddingStatus), nullable=False, default=EmbeddingStatus.PENDING)


__all__ = ["Project", "Context", "File", "UserProject", "UserContext", "UserFile", "ContextFile"]
