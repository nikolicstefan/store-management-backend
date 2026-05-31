from typing import Any, Mapping


class ValidationError(Exception):
    pass


def validate_required_params(query: Mapping[str, Any], required_params: list[str]) -> None:
    for param in required_params:
        if query.get(param) is None:
            raise ValidationError(f"Query parameter {param} is missing.")


def validate_required_fields(body: Mapping[str, Any], required_fields: list[str]) -> None:
    for field in required_fields:
        value = body.get(field)
        if value is None:
            raise ValidationError(f"Field {field} is missing.")
