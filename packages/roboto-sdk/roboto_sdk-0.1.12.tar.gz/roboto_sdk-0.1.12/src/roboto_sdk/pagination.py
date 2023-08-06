from typing import Any, Generic, Optional, TypeVar

import pydantic
from pydantic.generics import GenericModel

Model = TypeVar("Model")


class PaginatedList(GenericModel, Generic[Model]):
    items: list[Model]
    next_token: Any = None
    # If True, there are more items to be fetched; use `next_token` to fetch the next page.
    # If False, there are no more items to be fetched, even if `next_token` is defined.
    has_next: Optional[bool] = None

    @pydantic.validator("has_next", always=True)
    def set_has_next_if_undefined(cls, v, values, **kwargs):
        if v is not None:
            if v is True and "next_token" not in values:
                raise ValueError("`has_next` is True, but `next_token` is not defined.")
            return v

        if "next_token" in values and values["next_token"] is not None:
            return True

        return False
