from flask import Blueprint, Response, jsonify, request

from common.decorators import role_required
from common.validation import ValidationError
from customer.services import search_products
from customer.validation import validate_required_params

customer_bp = Blueprint("customer", __name__)


@customer_bp.route("/search", methods=["GET"])
@role_required("customer")
def search() -> tuple[Response, int]:
    query = request.args
    required_params = ["name", "category"]

    try:
        validate_required_params(query, required_params)
    except ValidationError as e:
        return jsonify(message=str(e)), 400

    products, categories = search_products(
        name=query.get("name"),
        category=query.get("category")
    )

    return jsonify(categories=categories, products=products), 200
