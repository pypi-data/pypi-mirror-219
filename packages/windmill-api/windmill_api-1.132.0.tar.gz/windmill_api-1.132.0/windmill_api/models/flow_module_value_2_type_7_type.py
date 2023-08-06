from enum import Enum


class FlowModuleValue2Type7Type(str, Enum):
    HTTP = "http"

    def __str__(self) -> str:
        return str(self.value)
