from enum import Enum, auto, unique

@unique
class FileStatus(str, Enum):
    PENDING = auto()
    FINISHED = auto()
    ARKIVED = auto()
    DELETED = auto()


@unique
class EmbeddingStatus(str, Enum):
    PENDING = auto()
    FINISHED = auto()
    FAILED = auto()


@unique
class DocumentEmbeddingDistanceMetric(str, Enum):
    COSINE = auto()
    EUCLIDEAN = auto()
    DOT = auto()


@unique
class DocumentSearchMode(str, Enum):
    SEARCH = auto()
    SEARCH_WITH_CITATIONS = auto()
    HYDE = auto()

@unique
class ProjectPermission(str, Enum):
    READ = auto()
    WRITE = auto()
    ADMIN = auto()
    OWNER = auto()

@unique
class ContextPermission(str, Enum):
    READ = auto()
    WRITE = auto()
    ADMIN = auto()
    OWNER = auto()
