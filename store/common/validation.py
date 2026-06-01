from typing import Any, Mapping


class ValidationError(Exception):
    pass


def validate_required_fields(body: Mapping[str, Any], required_fields: list[str]) -> None:
    for field in required_fields:
        if body.get(field) is None:
            raise ValidationError(f"Field {field} is missing.")


def validate_order_id(order_id: Any) -> None:
    if order_id is None:
        raise ValidationError("Missing order id.")

    if not isinstance(order_id, int) or order_id <= 0:
        raise ValidationError("Invalid order id.")
