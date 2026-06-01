from datetime import UTC, datetime
from typing import Any

from sqlalchemy.exc import SQLAlchemyError

from common.extensions import db
from common.models import *
from common.services import ServiceError


def search_products(name: str, category: str) -> tuple[list[dict[str, Any]], list[str]]:
    name = name.strip()
    category = category.strip()

    products = (
        Product.query
        .join(Product.categories)
        .filter(Product.name.ilike(f"%{name}%"))
        .filter(Category.name.ilike(f"%{category}%"))
        .distinct()
        .order_by(Product.id)
        .all()
    )

    categories = (
        Category.query
        .join(Category.products)
        .filter(Category.name.ilike(f"%{category}%"))
        .filter(Product.name.ilike(f"%{name}%"))
        .distinct()
        .order_by(Category.name)
        .all()
    )

    return [
        {
            "categories": sorted(category.name for category in product.categories),
            "id": product.id,
            "name": product.name,
            "price": product.price
        }
        for product in products
    ], [
        category.name
        for category in categories
    ]


def find_product(product_id: int) -> Product | None:
    return Product.query.get(product_id)


def create_order(requests: list[dict[str, Any]], customer_email: str) -> Order:
    order_item_inputs = []

    for request_number, request in enumerate(requests):
        product = find_product(request["id"])

        if product is None:
            raise ServiceError(f"Invalid product for request number {request_number}.")

        order_item_inputs.append((product, request["quantity"]))

    order = Order(
        timestamp=datetime.now(UTC),
        status="CREATED",
        total_price=0.0,
        customer_email=customer_email,
        courier_email=None
    )

    total_price = 0.0

    for product, quantity in order_item_inputs:
        price = product.price
        total_price += price * quantity

        OrderItem(
            order=order,
            product=product,
            price=price,
            quantity=quantity
        )

    order.total_price = total_price
    db.session.add(order)

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise

    return order


def get_customer_orders(customer_email: str) -> list[dict[str, Any]]:
    orders = (
        Order.query
        .filter_by(customer_email=customer_email)
        .order_by(Order.id)
        .all()
    )

    return [
        {
            "products": [
                {
                    "categories": sorted(category.name for category in order_item.product.categories),
                    "name": order_item.product.name,
                    "price": order_item.price,
                    "quantity": order_item.quantity
                }
                for order_item in order.order_items
            ],
            "price": order.total_price,
            "status": order.status,
            "timestamp": order.timestamp.isoformat(timespec="seconds").replace("+00:00", "Z")
        }
        for order in orders
    ]


def set_order_complete(order_id: int, customer_email: str) -> None:
    updated_rows = (
        Order.query
        .filter_by(
            id=order_id,
            status="PENDING",
            customer_email=customer_email
        )
        .update({
            "status": "COMPLETE"
        })
    )

    if updated_rows == 0:
        raise ServiceError("Invalid order id.")

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise
