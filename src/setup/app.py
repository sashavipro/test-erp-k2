from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.core.exceptions import AppError
from src.core.logger import logger
from src.apps.clients.routers import router as clients_router
from src.apps.products.routers import router as products_router
from src.apps.orders.routers import router as orders_router
from src.apps.frontend.routers import router as frontend_router
from src.setup.lifespan import lifespan

def create_app() -> FastAPI:
    """
    Builds and returns the FastAPI application with all routers and middlewares.
    """
    app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        logger.warning(f"AppError Handled: {exc.error_code} - {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error_code": exc.error_code, "message": exc.message}
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception(f"Unhandled Exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"error_code": "INTERNAL_SERVER_ERROR", "message": "An unexpected error occurred."}
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(clients_router, prefix="/api")
    app.include_router(products_router, prefix="/api")
    app.include_router(orders_router, prefix="/api")
    app.include_router(frontend_router)

    return app
