"""src/apps/frontend/routers.py."""

from pathlib import Path

from dishka.integrations.fastapi import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.apps.clients.services import ClientService
from src.apps.products.services import ProductService

router = APIRouter(tags=["frontend"])
templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=templates_dir)


@router.get("/", response_class=HTMLResponse)
@inject
async def index(
    request: Request,
    client_service: FromDishka[ClientService],
    product_service: FromDishka[ProductService],
):
    """Render index page."""
    clients = await client_service.get_clients()
    products = await product_service.get_products()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"clients": clients, "products": products},
    )
