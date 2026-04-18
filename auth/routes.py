from flask import Blueprint, jsonify, request, Response

from services import create_user
from validation import validate_registration_data, validate_email, validate_password, ValidationError

auth_bp = Blueprint("auth", __name__)


def register_user(role: str) -> tuple[Response, int]:
    data = request.get_json()

    try:
        validate_registration_data(data)
        validate_email(data.get("email"))
        validate_password(data.get("password"))
    except ValidationError as e:
        return jsonify(message=str(e)), 400
    
    create_user(
        forename=data.get("forename"),
        surname=data.get("surname"),
        email=data.get("email"),
        password=data.get("password"),
        role=role
    )

    return "", 200


@auth_bp.route("/register_customer", methods=["POST"])
def register_customer() -> tuple[Response, int]:
    return register_user("customer")


@auth_bp.route("/register_courier", methods=["POST"])
def register_courier() -> tuple[Response, int]:
    return register_user("courier")
