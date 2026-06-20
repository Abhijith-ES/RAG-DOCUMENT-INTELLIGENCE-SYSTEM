from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    document_id : str
    message : str
    num_chunks : int


class AskRequest(BaseModel):
    document_id : str = Field(
        min_length=1
    )
    query : str = Field(
        min_length=1
    )


class AskResponse(BaseModel):
    answer : str