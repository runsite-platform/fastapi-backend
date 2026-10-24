from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from app.config.db import DatabaseManager
from app.config.logger import logger
from app.config.settings import settings
from app.routes.router import api_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("Starting up")
    await DatabaseManager.setup()
    yield
    await DatabaseManager.stop()
    logger.info("Shutting down")


app = FastAPI(
    title="FastAPI Backend",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


app.include_router(api_router)
add_pagination(app)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
