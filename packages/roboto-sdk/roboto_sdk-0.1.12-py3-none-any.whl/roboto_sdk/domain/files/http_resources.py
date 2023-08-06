import pydantic


class CreateFileRequest(pydantic.BaseModel):
    bucket: str
    key: str


class DeleteFileRequest(pydantic.BaseModel):
    bucket: str
    key: str
