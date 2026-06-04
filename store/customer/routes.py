from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity

from common.decorators import role_required
from common.services import ServiceError
from common.validation import ValidationError, validate_order_id, validate_required_fields
from customer.services import create_order, get_customer_orders, search_products, set_order_complete
from customer.validation import validate_requests

customer_bp = Blueprint("customer", __name__)


@customer_bp.route("/search", methods=["GET"])
@role_required("customer")
def search() -> tuple[Response, int]:
    name = request.args.get("name", "")
    category = request.args.get("category", "")

    products, categories = search_products(
        name=name,
        category=category
    )

    return jsonify(categories=categories, products=products), 200


@customer_bp.route("/order", methods=["POST"])
@role_required("customer")
def order() -> tuple[Response, int]:
    body = request.get_json() or {}
    required_fields = ["requests"]

    try:
        validate_required_fields(body, required_fields)
        validate_requests(body["requests"])

        order = create_order(
            requests=body["requests"],
            customer_email=get_jwt_identity()
        )
    except (ValidationError, ServiceError) as e:
        return jsonify(message=str(e)), 400

    return jsonify(id=order.id), 200


@customer_bp.route("/status", methods=["GET"])
@role_required("customer")
def status() -> tuple[Response, int]:
    orders = get_customer_orders(get_jwt_identity())
    return jsonify(orders=orders), 200


@customer_bp.route("/delivered", methods=["POST"])
@role_required("customer")
def delivered() -> tuple[Response, int]:
    body = request.get_json() or {}

    try:
        validate_order_id(body.get("id"))

        set_order_complete(
            order_id=body["id"],
            customer_email=get_jwt_identity()
        )
    except (ValidationError, ServiceError) as e:
        return jsonify(message=str(e)), 400

    return jsonify(), 200
