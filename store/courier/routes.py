from flask import Blueprint, Response, jsonify

from common.decorators import role_required
from courier.services import get_orders_to_deliver

courier_bp = Blueprint("courier", __name__)


@courier_bp.route("/orders_to_deliver", methods=["GET"])
@role_required("COURIER")
def orders_to_deliver() -> tuple[Response, int]:
    orders = get_orders_to_deliver()
    return jsonify(orders=orders), 200
