from typing import Any

from sqlalchemy.exc import SQLAlchemyError

from common.extensions import db
from common.models import *
from common.services import ServiceError


def get_orders_to_deliver() -> list[dict[str, Any]]:
    orders = (
        Order.query
        .filter_by(status="CREATED")
        .order_by(Order.id)
        .all()
    )

    return [
        {
            "id": order.id,
            "email": order.customer_email
        }
        for order in orders
    ]


def set_order_pending(order_id: int, courier_email: str) -> None:
    updated_rows = (
        Order.query
        .filter_by(
            id=order_id,
            status="CREATED"
        )
        .update({
            "status": "PENDING",
            "courier_email": courier_email
        })
    )

    if updated_rows == 0:
        raise ServiceError("Invalid order id.")

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise
