from typing import Any, Mapping


class ValidationError(Exception):
    pass


def validate_required_fields(body: Mapping[str, Any], required_fields: list[str]) -> None:
    for field in required_fields:
        if body.get(field) is None:
            raise ValidationError(f"Field {field} is missing.")
