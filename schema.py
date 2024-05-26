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


class AbstractUser(pydantic.BaseModel, ABC):
    name: str
    password: str

    @pydantic.field_validator("password")
    @classmethod
    def length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError(f"Minimal length of password is 8")
        return v


class CreateUser(AbstractUser):
    name: str
    password: str


class UpdateUser(AbstractUser):
    name: Optional[str] = None
    password: Optional[str] = None


class CreateAd(AbstractAd):
    header: str
    description: Optional[str] = None


class UpdateAd(AbstractAd):
    header: Optional[str] = None
    description: Optional[str] = None
