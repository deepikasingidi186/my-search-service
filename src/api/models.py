from pydantic import BaseModel, Field
from typing import List


class Document(BaseModel):
    id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    tags: List[str] = []
