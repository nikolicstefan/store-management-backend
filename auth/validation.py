import re

from services import get_user_by_email


class ValidationError(Exception):
    pass


def validate_registration_data(data: dict[str, str]) -> None:
    required_fields = ["forename", "surname", "email", "password"]
    for field in required_fields:
        if not data.get(field):
            raise ValidationError(f"Field {field} is missing.")


def validate_email(email: str) -> None:
    if len(email) > 256 or not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        raise ValidationError("Invalid email.")
    if get_user_by_email(email):
        raise ValidationError("Email already exists.")


def validate_password(password: str) -> None:
    if len(password) < 8 or len(password) > 256:
        raise ValidationError("Invalid password.")
