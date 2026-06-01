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
