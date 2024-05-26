from typing import Type

from pydantic import ValidationError

from error_handler import HttpError
from schema import CreateAd, UpdateAd, CreateUser, UpdateUser


def validate_json(json_data: dict, schema_class: Type[CreateAd] | Type[UpdateAd] | Type[CreateUser] | Type[UpdateUser]):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)
