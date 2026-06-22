from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dishka.integrations.fastapi import FromDishka
import os

from src.apps.clients.services import ClientService
from src.apps.products.services import ProductService

router = APIRouter(tags=["frontend"])
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

@router.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    client_service: FromDishka[ClientService],
    product_service: FromDishka[ProductService]
):
    clients = await client_service.get_clients()
    products = await product_service.get_products()
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "clients": clients,
        "products": products
    })
