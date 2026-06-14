from pydantic import BaseModel

class Parameter(BaseModel):
    name: str
    label: str
    type: str
    default: float | int | str
    min: float | None = None
    max: float | None = None
    step: float | None = None