from abc import ABC
import pydantic
from typing import Optional


class AbstractAd(pydantic.BaseModel, ABC):
    header: str
    description: str

    @pydantic.field_validator("description")
    @classmethod
    def length(cls, v: str) -> str:
        if len(v) > 100:
            raise ValueError(f"Maximal length of description is 100")
        return v


class CreateAd(AbstractAd):
    header: str
    description: str


class UpdateAd(AbstractAd):
    header: Optional[str] = None
    description: Optional[str] = None