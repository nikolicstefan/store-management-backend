from re import match
from typing import Any, Mapping


class ValidationError(Exception):
    pass


def validate_required_fields(body: Mapping[str, Any], required_fields: list[str]) -> None:
    for field in required_fields:
        value = body.get(field)
        if value is None:
            raise ValidationError(f"Field {field} is missing.")


def validate_forename(forename: Any) -> None:
    if not isinstance(forename, str) or not forename.strip() or len(forename) > 256:
        raise ValidationError("Invalid forename.")


def validate_surname(surname: Any) -> None:
    if not isinstance(surname, str) or not surname.strip() or len(surname) > 256:
        raise ValidationError("Invalid surname.")


def validate_email(email: Any) -> None:
    regex = r'^[^@]+@[^@]+\.[^@]+$'
    if not isinstance(email, str) or not email.strip() or len(email) > 256 or not match(regex, email):
        raise ValidationError("Invalid email.")


def validate_password(password: Any) -> None:
    if not isinstance(password, str) or not password.strip() or len(password) < 8 or len(password) > 256:
        raise ValidationError("Invalid password.")
