from enum import Enum


class CompletedJobJobKind(str, Enum):
    SCRIPT = "script"
    PREVIEW = "preview"
    DEPENDENCIES = "dependencies"
    FLOW = "flow"
    FLOWPREVIEW = "flowpreview"
    SCRIPT_HUB = "script_hub"
    IDENTITY = "identity"
    HTTP = "http"

    def __str__(self) -> str:
        return str(self.value)
