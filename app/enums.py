from enum import Enum


class Language(str, Enum):
    KO = "ko"
    EN = "en"
    JA = "ja"

    def __str__(self):
        return self.value
