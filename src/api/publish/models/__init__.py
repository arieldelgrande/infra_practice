from pydantic import BaseModel

class PublishItem(BaseModel):
    name: str
    description: str

class PublishResponse(BaseModel):
    item: PublishItem
    status: str