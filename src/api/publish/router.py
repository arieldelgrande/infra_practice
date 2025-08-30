from fastapi import APIRouter
from src.api.publish.models import PublishItem, PublishResponse

publish_router = APIRouter(prefix="/publish", tags=["publish"])

@publish_router.post("/", response_model=PublishResponse)
def create_publish_item(item: PublishItem):
    return {"item": item, "status": "published"}
