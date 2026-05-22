from flask import Blueprint, Response, g, jsonify, request

from decorators import user_required
from security import create_token
from services import ServiceError, add_user, authenticate_user, delete_user_by_email
from validation import (
    ValidationError,
    validate_email,
    validate_forename,
    validate_password,
    validate_required_fields,
    validate_surname,
)

auth_bp = Blueprint("auth", __name__)


def register_user(role: str) -> tuple[Response, int]:
    body = request.get_json() or {}
    required_fields = ["forename", "surname", "email", "password"]

    try:
        validate_required_fields(body, required_fields)
        validate_forename(body.get("forename"))
        validate_surname(body.get("surname"))
        validate_email(body.get("email"))
        validate_password(body.get("password"))

        user = add_user(
            forename=body.get("forename"),
            surname=body.get("surname"),
            email=body.get("email"),
            password=body.get("password"),
            role=role
        )
    except (ValidationError, ServiceError) as e:
        return jsonify(message=str(e)), 400

    return jsonify(), 200


@auth_bp.route("/register_customer", methods=["POST"])
def register_customer() -> tuple[Response, int]:
    return register_user("customer")


@auth_bp.route("/register_courier", methods=["POST"])
def register_courier() -> tuple[Response, int]:
    return register_user("courier")


@auth_bp.route("/login", methods=["POST"])
def login() -> tuple[Response, int]:
    body = request.get_json() or {}
    required_fields = ["email", "password"]

    try:
        validate_required_fields(body, required_fields)
        validate_email(body.get("email"))

        user = authenticate_user(
            email=body.get("email"),
            password=body.get("password")
        )
    except (ValidationError, ServiceError) as e:
        return jsonify(message=str(e)), 400
    
    token = create_token(user)

    return jsonify(accessToken=token), 200


@auth_bp.route("/delete", methods=["POST"])
@user_required()
def delete() -> tuple[Response, int]:
    try:
        delete_user_by_email(g.user.email)
    except ServiceError as e:
        return jsonify(message=str(e)), 400

    return jsonify(), 200


# temporary route for testing
@auth_bp.route("/me", methods=["GET"])
@user_required()
def me() -> tuple[Response, int]:
    return jsonify({
        "email": g.user.email,
        "role": g.user.role
    }), 200
