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
