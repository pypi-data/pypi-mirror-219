# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ....core.datetime_utils import serialize_datetime


class OperatorSchema(pydantic.BaseModel):
    operator: typing.Optional[str] = pydantic.Field(description="The operator for which an operator schema is defined.")
    is_unique: typing.Optional[bool] = pydantic.Field(
        description="Whether the operator can be repeated multiple times."
    )

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        json_encoders = {dt.datetime: serialize_datetime}
