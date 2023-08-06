#  Copyright (c) 2023 Roboto Technologies, Inc.
import pydantic


class CreateTriggerRequest(pydantic.BaseModel):
    # Required
    name: str = pydantic.Field(regex=r"[\w\-]{1,256}")
    action_name: str
