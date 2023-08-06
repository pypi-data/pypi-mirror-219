from enum import Enum


class GetApiV1StudiesIdExportMethod(str, Enum):
    EMAIL = "EMAIL"

    def __str__(self) -> str:
        return str(self.value)
