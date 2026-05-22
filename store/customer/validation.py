from typing import Any, Mapping

from common.validation import ValidationError


def validate_required_params(query: Mapping[str, Any], required_params: list[str]) -> None:
    for param in required_params:
        if query.get(param) is None:
            raise ValidationError(f"Query parameter {param} is missing.")
