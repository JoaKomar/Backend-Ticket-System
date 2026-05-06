from pydantic import BaseModel, Field

#Schema of comment
class Comment(BaseModel):
    content: str = Field(max_length=600)

    