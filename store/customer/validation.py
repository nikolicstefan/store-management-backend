from typing import Any, Mapping

from common.validation import ValidationError


def validate_request_fields(request: Mapping[str, Any], required_fields: list[str], request_number: int) -> None:
    for field in required_fields:
        value = request.get(field)

        if value is None:
            raise ValidationError(f"Product {field} is missing for request number {request_number}.")

        if not isinstance(value, int) or value <= 0:
            raise ValidationError(f"Invalid product {field} for request number {request_number}.")


def validate_requests(requests: Any) -> None:
    if not isinstance(requests, list) or not requests:
        raise ValidationError("Invalid requests.")

    for request_number, request in enumerate(requests):
        if not isinstance(request, dict):
            raise ValidationError(f"Invalid request number {request_number}.")

        validate_request_fields(request, ["id", "quantity"], request_number)
