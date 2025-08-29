import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.config import settings
from src.common.utils.datetime import now

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug_mode,
    openapi_url=settings.openapi_url,
    docs_url=settings.docs_url,
)

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "Success": False,
            "timestamp": now().isoformat(),
            "detail": "Internal Server Error",
            "error": str(exc)
        },
    )

if __name__ == "__main__":
    
    if settings.env == "development":
        uvicorn.run("src.main:app", host="127.0.0.1", port=settings.port, reload=True)
    elif settings.env in ("staging", "production"):
        uvicorn.run("src.main:app", host="0.0.0.0", port=settings.port)