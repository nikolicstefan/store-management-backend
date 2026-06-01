from flask import Blueprint, Response, jsonify, request

from common.decorators import role_required
from common.services import ServiceError
from common.validation import ValidationError
from owner.services import create_products, get_product_statistics
from owner.validation import validate_file

owner_bp = Blueprint("owner", __name__)


@owner_bp.route("/update", methods=["POST"])
@role_required("OWNER")
def update() -> tuple[Response, int]:
    file = request.files.get("file")

    try:
        product_inputs = validate_file(file)
        create_products(product_inputs)
    except (ValidationError, ServiceError) as e:
        return jsonify(message=str(e)), 400
    
    return jsonify(), 200


@owner_bp.route("/product_statistics", methods=["GET"])
@role_required("OWNER")
def product_statistics() -> tuple[Response, int]:
    statistics = get_product_statistics()
    return jsonify(statistics=statistics), 200
