"""src/setup/lifespan.py."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager (startup/shutdown events).

    Dishka inherently manages DI scopes, but you can use this for
    other global state setup/teardown (e.g. disposing sqlalchemy engine, redis, etc).
    """
    logger.info("Starting up ERP application...")

    yield  # Application is running

    logger.info("Shutting down ERP application...")
