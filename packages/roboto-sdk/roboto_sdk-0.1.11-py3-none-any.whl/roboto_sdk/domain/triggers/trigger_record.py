#  Copyright (c) 2023 Roboto Technologies, Inc.


import pydantic


class TriggerRecord(pydantic.BaseModel):
    name: str
    org_id: str
    action_name: str
    """
    Coming soon:
    * Conditions
    * Repo override
    * Tag override
    """
