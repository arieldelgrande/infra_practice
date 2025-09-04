from fastapi import APIRouter
from src.api.publish.models import PublishItem, PublishResponse
from src.common.utils.observability.logger import logger
publish_router = APIRouter(prefix="/publish", tags=["publish"])


@publish_router.post("/", response_model=PublishResponse)
def create_publish_item(item: PublishItem):
    logger.info("Initializing publish item creation", ariel="delgrande")

    logger.info("Publish item created successfully")
    # Simulate some processing
    return {"item": item, "status": "published"}
