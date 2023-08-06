from enum import Enum


class ModelStatus(str, Enum):
    CONVERTING = "converting"
    ERROR = "error"
    PENDING_CONVERSION = "pending_conversion"
    READY = "ready"
    UPLOADING = "uploading"

    def __str__(self) -> str:
        return str(self.value)
