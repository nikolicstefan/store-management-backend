from re import match
from typing import Any, Mapping


class ValidationError(Exception):
    pass


def validate_required_fields(body: Mapping[str, Any], required_fields: list[str]) -> None:
    for field in required_fields:
        if body.get(field) is None:
            raise ValidationError(f"Field {field} is missing.")


def validate_required_string_fields(body: Mapping[str, Any], required_fields: list[str]) -> None:
    validate_required_fields(body, required_fields)

    for field in required_fields:
        value = body.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValidationError(f"Field {field} is missing.")


def validate_forename(forename: str) -> None:
    if len(forename) > 256:
        raise ValidationError("Invalid forename.")


def validate_surname(surname: str) -> None:
    if len(surname) > 256:
        raise ValidationError("Invalid surname.")


def validate_email(email: str) -> None:
    regex = r'^[^@]+@[^@]+\.[^@]+$'
    if len(email) > 256 or not match(regex, email):
        raise ValidationError("Invalid email.")


def validate_password(password: str) -> None:
    if len(password) < 8 or len(password) > 256:
        raise ValidationError("Invalid password.")
