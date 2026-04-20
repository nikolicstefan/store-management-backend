from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from security import create_token
from services import ServiceError, authenticate_user, create_user, delete_user_by_email
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
    data = request.get_json() or {}
    required_fields = ["forename", "surname", "email", "password"]

    try:
        validate_required_fields(data, required_fields)
        validate_forename(data.get("forename"))
        validate_surname(data.get("surname"))
        validate_email(data.get("email"))
        validate_password(data.get("password"))

        user = create_user(
            forename=data.get("forename"),
            surname=data.get("surname"),
            email=data.get("email"),
            password=data.get("password"),
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
    data = request.get_json() or {}
    required_fields = ["email", "password"]

    try:
        validate_required_fields(data, required_fields)
        validate_email(data.get("email"))

        user = authenticate_user(
            email=data.get("email"),
            password=data.get("password")
        )
    except (ValidationError, ServiceError) as e:
        return jsonify(message=str(e)), 400
    
    token = create_token(user)

    return jsonify(accessToken=token), 200


# temporary route for testing
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me() -> tuple[Response, int]:
    return jsonify({
        "identity": get_jwt_identity(),
        "claims": get_jwt()
    }), 200


@auth_bp.route("/delete", methods=["POST"])
@jwt_required()
def delete() -> tuple[Response, int]:
    try:
        email = get_jwt_identity()
        delete_user_by_email(email)
    except ServiceError as e:
        return jsonify(message=str(e)), 400

    return jsonify(),200
