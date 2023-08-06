from enum import Enum


class CreateStudyPeripheralRequirementsItem(str, Enum):
    AUDIO = "audio"
    CAMERA = "camera"
    DOWNLOAD = "download"
    MICROPHONE = "microphone"

    def __str__(self) -> str:
        return str(self.value)
