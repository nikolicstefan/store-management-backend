import re

from typing import Any, Mapping


class ValidationError(Exception):
    pass


def validate_required_fields(data: Mapping[str, Any], required_fields: list[str]) -> None:
    for field in required_fields:
        value = data.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValidationError(f"Field {field} is missing.")


def validate_forename(forename: Any) -> None:
    if not isinstance(forename, str) or len(forename) > 256:
        raise ValidationError("Invalid forename.")


def validate_surname(surname: Any) -> None:
    if not isinstance(surname, str) or len(surname) > 256:
        raise ValidationError("Invalid surname.")


def validate_email(email: Any) -> None:
    if not isinstance(email, str) or len(email) > 256 or not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        raise ValidationError("Invalid email.")


def validate_password(password: Any) -> None:
    if not isinstance(password, str) or len(password) < 8 or len(password) > 256:
        raise ValidationError("Invalid password.")
