from enum import Enum


class CreateStudyDeviceCompatibilityItem(str, Enum):
    DESKTOP = "desktop"
    MOBILE = "mobile"
    TABLET = "tablet"

    def __str__(self) -> str:
        return str(self.value)
