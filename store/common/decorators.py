from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required
from flask_jwt_extended.exceptions import NoAuthorizationError


def role_required(role: str):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()

            if claims.get("roles") != role:
                raise NoAuthorizationError("Missing Authorization Header")

            return fn(*args, **kwargs)

        return wrapper

    return decorator
