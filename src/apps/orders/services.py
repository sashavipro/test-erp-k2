from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from decimal import Decimal

from src.apps.orders.schemas import OrderCreate, OrderResponse
from src.apps.orders.repositories import OrderRepository
from src.apps.orders.models import Order, OrderItem
from src.core.exceptions import ClientNotFoundError, ProductNotFoundError
from src.core.logger import logger

class OrderService:
    """
    Service class for managing Order-related business logic, including 
    automatic calculation of total amounts and validation of items.
    """
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    async def create_order(self, order_in: OrderCreate) -> OrderResponse:
        """
        Creates a new order for a client. Validates the existence of the client
        and products, and automatically computes the total amount based on product prices.
        """
        logger.info(f"Attempting to create order for client: {order_in.client_id}")
        # Check if client exists
        client = await self.repo.get_client_by_id(order_in.client_id)
        if not client:
            raise ClientNotFoundError()

        product_ids = [item.product_id for item in order_in.items]
        products = await self.repo.get_products_by_ids(product_ids)
        
        products_dict = {p.id: p for p in products}
        
        total_amount = Decimal('0.0')
        order_items = []
        
        # We need the order id before creating items? Actually we can create Order, add items to its `items` relationship.
        # But we create them together.
        order = Order(client_id=order_in.client_id, total_amount=total_amount)
        
        for item_in in order_in.items:
            product = products_dict.get(item_in.product_id)
            if not product:
                raise ProductNotFoundError()
            
            total_amount += product.price * item_in.quantity
            order_item = OrderItem(
                order=order,
                product_id=product.id,
                quantity=item_in.quantity
            )
            order_items.append(order_item)

        order.total_amount = total_amount
        logger.info(f"Successfully created order with total amount: {total_amount} for client: {order_in.client_id}")
        return await self.repo.create(order, order_items)

    async def get_orders_for_client(self, client_id: UUID) -> List[OrderResponse]:
        """
        Retrieve all orders associated with a given client ID.
        Raises HTTP 404 if the client is not found.
        """
        client = await self.repo.get_client_by_id(client_id)
        if not client:
            raise ClientNotFoundError()
        return await self.repo.get_orders_by_client(client_id)
