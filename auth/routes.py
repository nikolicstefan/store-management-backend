from flask import Blueprint, Response, g, jsonify, request

from decorators import user_required
from security import create_token
from services import create_user, authenticate_user, delete_user
from validation import (
    validate_email,
    validate_forename,
    validate_password,
    validate_required_string_fields,
    validate_surname,
)

auth_bp = Blueprint("auth", __name__)


def register_user(role: str) -> tuple[Response, int]:
    body = request.get_json() or {}
    required_fields = ["forename", "surname", "email", "password"]

    validate_required_string_fields(body, required_fields)
    validate_forename(body["forename"])
    validate_surname(body["surname"])
    validate_email(body["email"])
    validate_password(body["password"])

    user = create_user(
        forename=body["forename"],
        surname=body["surname"],
        email=body["email"],
        password=body["password"],
        role=role
    )

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

    validate_required_string_fields(body, required_fields)
    validate_email(body["email"])

    user = authenticate_user(
        email=body["email"],
        password=body["password"]
    )

    token = create_token(user)

    return jsonify(accessToken=token), 200


@auth_bp.route("/delete", methods=["POST"])
@user_required()
def delete() -> tuple[Response, int]:
    delete_user(g.user.email)
    return jsonify(), 200


# temporary route for testing
@auth_bp.route("/me", methods=["GET"])
@user_required()
def me() -> tuple[Response, int]:
    return jsonify({
        "email": g.user.email,
        "role": g.user.role
    }), 200
