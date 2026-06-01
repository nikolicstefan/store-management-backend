from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity

from common.decorators import role_required
from common.services import ServiceError
from common.validation import ValidationError, validate_order_id
from courier.services import get_orders_to_deliver, set_order_pending

courier_bp = Blueprint("courier", __name__)


@courier_bp.route("/orders_to_deliver", methods=["GET"])
@role_required("COURIER")
def orders_to_deliver() -> tuple[Response, int]:
    orders = get_orders_to_deliver()
    return jsonify(orders=orders), 200


@courier_bp.route("/pick_up_order", methods=["POST"])
@role_required("COURIER")
def pick_up_order() -> tuple[Response, int]:
    body = request.get_json() or {}

    try:
        validate_order_id(body.get("id"))

        set_order_pending(
            order_id=body["id"],
            courier_email=get_jwt_identity()
        )
    except (ValidationError, ServiceError) as e:
        return jsonify(message=str(e)), 400

    return jsonify(), 200
