from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.config import settings
from src.common.utils.datetime import now
from src.api.publish.router import publish_router  
from src.common.utils.observability.middleware import Observability
from src.common.utils.observability.logger import logger 

observability = Observability(tracer_name="publish_tracer", meter_name="publish_metric")


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug_mode,
    openapi_url=settings.openapi_url,
    docs_url=settings.docs_url,
    root_path="/api/v1",
)


app.include_router(publish_router)


@app.get("/health", tags=["health"])
def health_check():

    observability.create_traced_publish_item({"service.name": settings.app_name, "environment": settings.env, "status": "healthy"})
    observability.create_metric_publish_item({"service.name": settings.app_name, "environment": settings.env, "status": "healthy"})
    logger.info("Health check endpoint called")
    return {"status": "ok", "env": settings.env, "timestamp": now().isoformat()}


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "Success": False,
            "timestamp": now().isoformat(),
            "detail": "Internal Server Error",
            "error": str(exc),
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    missing_fields = []
    for error in exc.errors():
        if error["type"] == "missing":
            missing_fields.append(error["loc"][-1])
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "missing_fields": missing_fields,
            "detail": exc.errors(),
        },
    )

# FastAPIInstrumentor.instrument_app(app)
