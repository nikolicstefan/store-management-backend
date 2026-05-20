from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required


def role_required(role: str):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()

            if claims.get("role") != role:
                return jsonify(message=f"{role.capitalize()} role required."), 403

            return fn(*args, **kwargs)

        return wrapper

    return decorator
