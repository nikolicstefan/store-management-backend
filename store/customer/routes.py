from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity

from common.decorators import role_required
from common.services import ServiceError
from common.validation import ValidationError, validate_required_fields, validate_required_params
from customer.services import create_order, search_products
from customer.validation import validate_requests

customer_bp = Blueprint("customer", __name__)


@customer_bp.route("/search", methods=["GET"])
@role_required("CUSTOMER")
def search() -> tuple[Response, int]:
    query = request.args
    required_params = ["name", "category"]

    try:
        validate_required_params(query, required_params)
    except ValidationError as e:
        return jsonify(message=str(e)), 400

    products, categories = search_products(
        name=query["name"],
        category=query["category"]
    )

    return jsonify(categories=categories, products=products), 200


@customer_bp.route("/order", methods=["POST"])
@role_required("CUSTOMER")
def order() -> tuple[Response, int]:
    body = request.get_json() or {}
    required_fields = ["requests"]

    try:
        validate_required_fields(body, required_fields)
        validate_requests(body.get("requests"))

        order = create_order(
            requests=body["requests"],
            customer_email=get_jwt_identity()
        )
    except (ValidationError, ServiceError) as e:
        return jsonify(message=str(e)), 400

    return jsonify(id=order.id), 200
