import uvicorn
from fastapi import FastAPI

from application.core.config import settings
from application.api.routers import router as api_router


main_app = FastAPI()

main_app.include_router(
    api_router
)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True)
