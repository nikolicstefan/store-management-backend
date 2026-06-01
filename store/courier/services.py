from typing import Any

from common.models import *


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
